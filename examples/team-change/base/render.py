"""Render an exported order from stdin."""

import json
import sys


if __name__ == "__main__":
    order = json.load(sys.stdin)
    print(order["order"], order["total_cents"])
