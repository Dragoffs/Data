#!/usr/bin/python3
import argparse
from typing import *
import datetime as dt
from parse import parse
import sys
import re

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

ARGS = parser.parse_args()

def parse_log(log_fn: str, out_fn: str, timestamp: dt.datetime) -> None:
    # How to delineate between other logging and ssh-related logging?
    # Using timestamp, scan new / changed lines and add to the database
    # Side effect: write to MongoDB via API

    pass

def main() -> int:
    log_fn = ARGS.logfile
    time_fn = ARGS.timestamp
    out_fn = ARGS.output

    # Jan 1st, year 1 by default
    timestamp = dt.datetime(1, 1, 1) 

    # Load last timestamp
    with open(time_fn, 'r') as time_fp:
        line = time_fp.readline()

        if line == "":
            print("ERROR: Timestamp file '{}' is empty.".format(time_fn), file=sys.stderr)
            return 1
        
        result = parse("{timestamp:ts}", line.strip()) # returns a datetime object
        timestamp = result['timestamp']

    # scan file until a time greater than the last timestamp was found
    # Parse out any login attempts beyond this point and write to the database
    parse_log(log_fn, out_fn, timestamp)


if __name__ == "__main__":
    main()
