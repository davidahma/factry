"""Render an exported order from stdin."""

import argparse
from dataclasses import dataclass
import json
import sys


@dataclass
class Order:
    order: str
    total_cents: int


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", action="store_true")
    args = parser.parse_args()
    payload = json.load(sys.stdin)
    order = Order(**payload)
    if args.receipt:
        dollars, cents = divmod(order.total_cents, 100)
        print(f"{order.order} ${dollars}.{cents:02}")
    else:
        print(order.order, order.total_cents)
