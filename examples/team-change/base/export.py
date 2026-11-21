"""Export one example order as JSON."""

import argparse
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export an order.")
    parser.add_argument("--cents", type=int, default=1250)
    args = parser.parse_args()
    if args.cents < 0:
        parser.error("--cents must be nonnegative")
    print(json.dumps({"order": "A-17", "total_cents": args.cents}))
