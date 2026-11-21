"""Make four small Git projects for the engineering-skill trials."""

import argparse
import os
from pathlib import Path
import subprocess
from textwrap import dedent


CHANNEL = {
    "README.md": """
        # Radio channel records

        `python3 channel.py N` prints the unsigned two-byte network encoding of
        a channel as four lowercase hex digits. Every integer from 0 through
        65535 is supported. Run `python3 -B -m unittest -v` to check the project.
    """,
    "test_channel.py": '''
        import subprocess
        import sys
        import unittest


        class ChannelTest(unittest.TestCase):
            def test_control_channels(self):
                for value, expected in [(0, "0000"), (260, "0104")]:
                    with self.subTest(value=value):
                        data = subprocess.check_output([sys.executable, "channel.py", str(value)])
                        self.assertEqual(data.decode().strip(), expected)
    ''',
}
CHANNEL_UPDATE = {
    "channel.py": '''
        import struct
        import sys


        def encode(number):
            return struct.pack(">h", number)


        if __name__ == "__main__":
            print(encode(int(sys.argv[1])).hex())
    ''',
}
MIGRATION = {
    "README.md": """
        # Field ledger

        Collectors append one JSON object per line to a shared log. The billing
        process reads old and new records from that log. Collectors and billing
        deploy on different schedules. An operator can roll either back one
        version without warning. The log is the system of record and must remain
        readable after rollback. The current collector writes only GBP amounts.
        The next format renames the GBP minor-unit field to amount_minor.
    """,
    "collector.py": '''
        import json


        def append(stream, pence):
            stream.write(json.dumps({"total_pence": pence}) + "\\n")
    ''',
    "billing.py": '''
        import json


        def total(records):
            return sum(json.loads(line)["total_pence"] for line in records)
    ''',
    "test_ledger.py": '''
        from io import StringIO
        import unittest

        from billing import total
        from collector import append


        class BillingTest(unittest.TestCase):
            def test_total(self):
                stream = StringIO()
                append(stream, 3)
                append(stream, 5)
                self.assertEqual(total(stream.getvalue().splitlines()), 8)
    ''',
}
BASE_NOTICE = '''
    def deliver(record, sent, queue):
        queue.append(record)
'''
RETRY = {
    "README.md": """
        # Outbox

        Two records can have the same text. The local sent set tracks record IDs.
        The durable queue appends requests and does no deduplication. A queue
        append can succeed and its acknowledgement can be lost. Callers retry
        undelivered requests. Deliver each record once.
    """,
    "outbox.py": BASE_NOTICE,
}
RETRY_UPDATE = {
    "outbox.py": '''
        def deliver(record, sent, queue):
            if record["id"] in sent:
                return
            queue.append(record)
            sent.add(record["id"])
    ''',
    "test_outbox.py": '''
        import unittest

        from outbox import deliver


        class OutboxTest(unittest.TestCase):
            def test_repeated_success(self):
                sent, queue = set(), []
                record = {"id": "17", "text": "ready"}
                deliver(record, sent, queue)
                deliver(record, sent, queue)
                self.assertEqual(queue, [record])
    ''',
}
DOCS = {
    "README.md": """
        # Milepost

        Run `python3 milepost.py stats` to print the number of trail markers.
    """,
    "milepost.py": '''
        import argparse


        if __name__ == "__main__":
            parser = argparse.ArgumentParser()
            parser.add_argument("action", choices=["count"])
            parser.parse_args()
            print(3)
    ''',
}
# Each project has an ordinary main branch and, where relevant, a change to inspect.
PROJECTS = {
    "channel": (CHANNEL, CHANNEL_UPDATE),
    "ledger": (MIGRATION, {}),
    "outbox": (RETRY, RETRY_UPDATE),
    "milepost": (DOCS, {}),
}


def git(project, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_DATE="2024-02-01T00:00:00Z", GIT_COMMITTER_DATE="2024-02-01T00:00:00Z")
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                    "-c", "commit.gpgsign=false", "-c", "core.autocrlf=false", *args],
                   cwd=project, env=env, check=True, stdout=subprocess.DEVNULL)


def write_commit(project, files, message):
    for name, body in files.items():
        (project / name).write_bytes(dedent(body).strip().encode("utf-8") + b"\n")
    git(project, "add", ".")
    git(project, "commit", "-qm", message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path, help="new directory for the four checkouts")
    dest = parser.parse_args().destination
    dest.mkdir()
    for name, (base, change) in PROJECTS.items():
        project = dest / name
        project.mkdir()
        git(project, "init", "-q", "-b", "main")
        write_commit(project, base, "Initial project")
        if change:
            git(project, "checkout", "-qb", "candidate")
            write_commit(project, change, "Update implementation")
        print(project)


if __name__ == "__main__":
    main()
