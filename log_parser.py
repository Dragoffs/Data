#!/usr/bin/python3
import argparse
from typing import *
import datetime as dt
from parse import parse
import sys
import re
import json
from dataclasses import dataclass

parser = argparse.ArgumentParser(description="Extract login failure/success for user from log file and write to database") 
parser.add_argument(
        "logfile",
        type=str,
        help="Relative / absolute path to syslog or other log file"
)
parser.add_argument(
        "--timestamp",
        "-t",
        default="timestamp",
        type=str,
        help="Relative / absolute path to a timestamp file\n\tDefault: ./timestamp"
)
parser.add_argument(
        "--output",
        "-o",
        default="results.json",
        type=str,
        help="Relative / absolute path to a file to hold JSON output"
)

@dataclass
class RegexEntry:
    login_status: bool
    re: re.Pattern

ARGS = parser.parse_args()
SSHD_RE = re.compile(r"sshd\[\d+\]")

FAILED_PASSWORD_RE = re.compile(r"Failed password for (\w+)\s")
ACCEPTED_PASSWORD_RE = re.compile(r"Accepted password for (\w+)\s")
#AUTH_FAIL_RE = re.compile(r"authentication failure;.*user=(.+)")
# OTHER FAILURES? Network failure, etc.???

RE_LIST = [
    # Accept = True, Failure = False
    RegexEntry(True, ACCEPTED_PASSWORD_RE),
    RegexEntry(False, FAILED_PASSWORD_RE),
]


# Insert or initialize
def update_dict(d: dict, user: str, success: bool) -> dict:
    key = "successes" if success else "failures"

    if user not in d:
        d[user] = {"successes": 0, "failures": 0}

    d[user][key] += 1

    return d

def parse_log(log_fn: str, out_fn: str, timestamp: dt.datetime) -> None:
    # Using timestamp, scan new / changed lines and add to the database
    # Side effect: write to MongoDB via API
    # Save most recent timestamp in a buffer and return it when the function is finished

    login_dict = {}
    line = ""
    
    # Parse log
    with open(log_fn, "r") as log_fp:
        curr_ts = None # current timestamp
        line = log_fp.readline()

        # Read lines until the last timestamp is exceeded
        # TODO figure out how to quickly read out the timestamp, will also help with storing most recent timestamp for return
#        while curr_ts == None or curr_ts < timestamp:
#            line = log_fp.readline()
#            result = parse("{timestamp:ts}", line.strip())
#            curr_ts = result["timestamp"]
#
        # Read the rest of the file
        while line != "":
            if SSHD_RE.search(line) != None:

                # Parse line and add to dict
                for entry in RE_LIST:
                    login_status = entry.login_status
                    result = entry.re.search(line)
                    
                    if result != None:
                        user = result.groups(0)[0]
                        login_dict = update_dict(login_dict, user, login_status)
                        break

            # Continue reading lines
            line = log_fp.readline()

    # write dict out to json, to be replaced with calls to mongodb api
    with open(out_fn, 'w') as out_fp:
        json.dump(login_dict, out_fp)


def main() -> int:
    log_fn = ARGS.logfile
    time_fn = ARGS.timestamp
    out_fn = ARGS.output

    # Jan 1st, year 1 by default
    timestamp = dt.datetime(1, 1, 1) 

    # Load last timestamp
    with open(time_fn, "r") as time_fp:
        line = time_fp.readline()

        if line == "":
            print("ERROR: Timestamp file '{}' is empty.".format(time_fn), file=sys.stderr)
            return 1
        
        result = parse("{timestamp:ts}", line.strip()) # returns a datetime object
        timestamp = result["timestamp"]

    # scan file until a time greater than the last timestamp was found
    # Parse out any login attempts beyond this point and write to the database
    new_ts = parse_log(log_fn, out_fn, timestamp)

    # write new timestamp to a file

    return 0

if __name__ == "__main__":
    main()
