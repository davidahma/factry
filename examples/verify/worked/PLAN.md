# Repair the line limit

The caller pipes bytes into `lines.py` and selects an optional maximum number of lines. Keep the existing CLI flags and error behavior. Limit the repair to the iterator in `lines.py` and the CLI regression tests.

| Caller request | Observation through stdin and stdout |
| --- | --- |
| Omit the option | Mixed line endings, non-UTF-8 bytes, and a final line without a newline survive unchanged. |
| Select a positive limit | A limit of two emits the first two lines in order. A limit larger than `sys.maxsize` exits successfully at EOF and preserves the available bytes. |
| Select zero | Nonempty input produces zero bytes and exits successfully. |
| Select a negative limit | The command exits with its existing usage error and leaves stdout empty. |

Add boundary tests through the CLI and run them against the current candidate. Change the line-selection logic to distinguish zero from an omitted limit and to accept the parser's large integers. Run the repository suite on the repaired revision.
