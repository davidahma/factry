"""Write or total receipt records on the command line."""

import argparse
import json
import sys


def encode(amount):
    return json.dumps({"total_pence": amount})


def total(records):
    return sum(json.loads(line)["total_pence"] for line in records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="action", required=True)
    writer = commands.add_parser("write")
    writer.add_argument("amount", type=int)
    commands.add_parser("total")
    args = parser.parse_args()
    if args.action == "write":
        print(encode(args.amount))
    else:
        print(total(sys.stdin))


if __name__ == "__main__":
    main()
