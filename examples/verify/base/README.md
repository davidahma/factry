# Lines

`lines.py` copies lines from standard input to standard output. It runs on Python 3 using only the standard library.

## Requested change

Add a `--limit N` option for scripting.

- With no option, preserve the input exactly.
- For a positive integer, print up to that many lines in their original order.
- For zero, exit successfully with empty output, even when input is available.

Run the native checks with `python3 -m unittest -v`.
