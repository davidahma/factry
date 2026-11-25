# Receipt ledger

`ledger.py` writes receipts as newline-delimited JSON and totals the receipts it reads from standard input. Amounts are integer GBP minor units.

```sh
python3 ledger.py write 125 | python3 ledger.py totals
```

The receipt total in this example is `125`.
