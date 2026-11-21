import argparse
import sys
from itertools import islice


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be nonnegative")

    lines = islice(sys.stdin.buffer, args.limit) if args.limit else sys.stdin.buffer
    sys.stdout.buffer.writelines(lines)


if __name__ == "__main__":
    main()
