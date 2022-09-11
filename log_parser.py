#!/usr/bin/python3
import argparse
from typing import *
import datetime as dt
from parse import parse
import sys
import re
import json
from dataclasses import dataclass
import os

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
TS_RE = re.compile(r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+([1-3]?[0-9])\s+([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])")

INVALID_USER_PASSWORD_RE = re.compile(r"Failed password for invalid user (\w+)\s")
FAILED_PASSWORD_RE = re.compile(r"Failed password for (\w+)\s")
ACCEPTED_PASSWORD_RE = re.compile(r"Accepted password for (\w+)\s")

RE_LIST = [
    RegexEntry(False, INVALID_USER_PASSWORD_RE), # Should be checked before others
    RegexEntry(True, ACCEPTED_PASSWORD_RE),
    RegexEntry(False, FAILED_PASSWORD_RE),
]


# Insert or initialize
"""
{
    user:
    {
        "Month Day":
        [
            {
                "result": "failure",
                "time": "00:00:00"
            },

            {
                " "
            },
            ...
        ]
        ...
    }
}
"""
def update_dict(d: dict, user: str, success: bool, timestamp: dt.datetime) -> dict:
    result = "success" if success else "failure"
    date = "{:02d}/{:02d}".format(timestamp.month, timestamp.day)
    time = "{:02d}:{:02d}:{:02d}".format(timestamp.hour, timestamp.minute, timestamp.second)

    if user not in d:
        d[user] = {}

        if date not in d[user]:
            d[user][date] = []

    d[user][date].append({"result": result, "time": time})

    return d

# Using timestamp, scan new / changed lines and add to the database
# Side effect: write to MongoDB via API
# Save most recent timestamp in a buffer and return it when the function is finished
def parse_log(log_fn: str, out_fn: str, timestamp: dt.datetime) -> None:
    login_dict = {}
    line = ""
    curr_ts = None
    
    with open(log_fn, "r") as log_fp:
        line = log_fp.readline()
        # Current timestamp (search for timestamp string in line, convert to timestamp with 'parse' library)
        ts_result = TS_RE.search(line)
        if ts_result != None:
            curr_ts = parse("{timestamp:ts}", ts_result.group(0))["timestamp"]

        # Read lines until the loaded timestamp is exceeded
        while curr_ts == None or curr_ts < timestamp:
            line = log_fp.readline()
            ts_result = TS_RE.search(line)
            if ts_result != None:
                curr_ts = parse("{timestamp:ts}", ts_result.group(0))["timestamp"]

        # Read the rest of the file
        while line != "":

            # Don't parse if its not an sshd line
            if SSHD_RE.search(line) != None:

                # Parse line and add to dict
                for entry in RE_LIST:
                    re_result = entry.re.search(line)
                    
                    if re_result != None:
                        login_status = entry.login_status
                        user = re_result.groups(0)[0]
                        login_dict = update_dict(login_dict, user, login_status, curr_ts)
                        break

            # Continue reading
            line = log_fp.readline()
            ts_result = TS_RE.search(line)
            if ts_result != None:
                curr_ts = parse("{timestamp:ts}", ts_result.group(0))["timestamp"]

    # write dict out to json, to be replaced with calls to mongodb api
    with open(out_fn, 'w') as out_fp:
        json.dump(login_dict, out_fp)

    # write out to timestamp file
    print(curr_ts)


def main() -> int:
    log_fn = ARGS.logfile
    time_fn = ARGS.timestamp
    out_fn = ARGS.output

    # Jan 1st, year 1 by default
    timestamp = dt.datetime(1, 1, 1) 

    # Load last timestamp
    if not os.path.exists(time_fn):
        print("ERROR: no timestamp file with name '{}'".format(time_fn))
        return 1

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
