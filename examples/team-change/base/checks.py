import subprocess
import sys


def cli(script, *args, data=b""):
    result = subprocess.run(
        [sys.executable, "-I", script, *args], input=data, capture_output=True,
    )
    if result.returncode or result.stderr:
        raise AssertionError(result.stderr.decode())
    return result.stdout
