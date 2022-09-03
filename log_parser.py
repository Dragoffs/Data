#!/usr/bin/python3
import argparse
from typing import *
import pickle

parser = argparse.ArgumentParser(description="Extract login failure/success for user from log file and write to database") 
parser.add_argument(
        "logfile",
        type=str,
        help="Relative / absolute path to"
)


def parse_log(fp, diffs: List[Tuple]) -> None:
    # Using diffs, scan new / changed lines and add to the database
    # Side effect: write to MongoDB via API
    pass

def main():
    # Load last timestamp
    # scan file until a time greater than the last timestamp was found
    # Parse out any login attempts beyond this point and write to the database

    # How to delineate between other logging and ssh-related logging?

    pass

if __name__ == "__main__":
    main()
