# Order export and rendering

`python3 export.py` writes a JSON object for order A-17 with an integer
`total_cents` of 1250. Use `--cents N` to supply a nonnegative whole number
of cents. All amounts in this exercise are US dollars.

`python3 render.py` reads one exported order from stdin. Its default output is
the order ID, a space, the integer cents and a newline. Additional JSON fields
are allowed. A renderer consumes the fields it needs.

Run the repository checks with `python3 -m unittest -v` in a clone.
