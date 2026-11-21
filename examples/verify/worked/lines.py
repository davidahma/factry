import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.limit is not None and args.limit < 0:
        parser.error("--limit must be nonnegative")

    if args.limit is None:
        sys.stdout.buffer.writelines(sys.stdin.buffer)
    else:
        for _, line in zip(range(args.limit), sys.stdin.buffer):
            sys.stdout.buffer.write(line)


if __name__ == "__main__":
    main()
