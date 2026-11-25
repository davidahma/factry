# Introduce the new receipt amount field

Update the ledger writer to use `amount_minor` as its field name. Change the reader to accept the new field and keep reading historical `total_pence` records. Leave both commands and their output shape alone.

Add coverage for one receipt written by the CLI with the new field, then test the total for a mixture of old and new rows. Run `python3 -B -m unittest discover -s tests -v`. Leave the patch unstaged.
