"""Create a two-developer order CLI exercise in a fresh temporary directory."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile


HERE = Path(__file__).resolve().parent
ROUND_TRIP = "test_default_round_trip"
CURRENCY = "test_currency_and_cents"
RECEIPT = "test_receipt_from_export"
HELP = "test_export_help"
EXTENSIONS = "test_renderer_accepts_additional_fields"
FILES = {
    "base": (".gitignore", "CONTRACT.md", "export.py", "render.py", "checks.py", "test_orders.py"),
    "producer": ("test_export.py",),
    "consumer": ("render.py", "test_render.py"),
    "control": ("test_help.py",),
    "worked": ("test_extensions.py",),
}


def git(repo, *args):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    empty_home = str(repo / ".git" / "empty-home")
    env.update(HOME=empty_home, XDG_CONFIG_HOME=empty_home,
               GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
               GIT_AUTHOR_DATE="2025-01-01T12:00:00Z", GIT_COMMITTER_DATE="2025-01-01T12:00:00Z",
               GIT_ATTR_NOSYSTEM="1", GIT_ALLOW_PROTOCOL="file", LC_ALL="C")
    result = subprocess.run(
        ["git", "-c", "core.hooksPath=" + os.devnull, "-c", "core.attributesFile=" + os.devnull,
         "-C", str(repo), *args], env=env, capture_output=True, text=True, timeout=30,
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} in {repo}: {result.stderr}")
    return result.stdout.strip()


def clone(root, directory, name):
    repo = root / directory
    git(root, "clone", "--no-local", "--template=", str(root / "origin.git"), str(repo))
    git(repo, "config", "user.name", name)
    git(repo, "config", "user.email", directory + "@example.invalid")
    git(repo, "config", "commit.gpgSign", "false")
    return repo


def apply_stage(repo, stage, subject, edit=None):
    for name in FILES[stage]:
        shutil.copyfile(HERE / stage / name, repo / name)
    if edit:
        filename, before, after = edit
        path = repo / filename
        source = path.read_text(encoding="utf-8")
        if source.count(before) != 1:
            raise RuntimeError(f"Expected one occurrence of {before!r} in {filename}")
        path.write_text(source.replace(before, after), encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-m", subject)
    return git(repo, "rev-parse", "HEAD")


def plain_output_env():
    env = os.environ.copy()
    env.pop("FORCE_COLOR", None)
    env["NO_COLOR"] = "1"
    return env


def check_suite(repo, label, head, passed, failed=()):
    if git(repo, "rev-parse", "HEAD") != head or git(repo, "status", "--porcelain"):
        raise RuntimeError("Expected clean checkout at " + head)
    result = subprocess.run([sys.executable, "-I", "-B", "-m", "unittest", "-v"],
                            cwd=repo, env=plain_output_env(), capture_output=True, text=True, timeout=30)
    expected = {name: "ok" for name in passed}
    expected.update({name: "FAIL" for name in failed})
    observed = re.findall(r"^(test_\w+) \([^\n]*\) \.\.\. (\w+)$", result.stderr, re.MULTILINE)
    if (result.returncode != int(bool(failed)) or len(observed) != len(expected)
            or dict(observed) != expected
            or f"Ran {len(expected)} test" not in result.stderr
            or (failed and result.stderr.count("unexpected keyword argument 'currency'") != len(failed))):
        raise RuntimeError(f"Unexpected native suite outcome for {label} at {head}\n{result.stderr}")
    print(f"{label} {head}  " + ", ".join(f"{test}={status}" for test, status in observed))
    if failed:
        print("  Both CLI paths rejected the additional 'currency' field.")
    if git(repo, "status", "--porcelain") or git(repo, "rev-parse", "HEAD") != head:
        raise RuntimeError("Suite changed the checkout")


def merge(repo, name, base, head):
    git(repo, "checkout", "-b", name, base)
    git(repo, "merge", "--no-ff", "-m", "Test " + name, head)
    revision = git(repo, "rev-parse", "HEAD")
    if git(repo, "show", "-s", "--format=%P", revision).split() != [base, head]:
        raise RuntimeError("Unexpected parents for " + name)
    print(f"{name} parents: base={base} head={head}")
    return revision


def probe_receipts(repo, *, exports_currency, accepts_extensions):
    def run(script, args, data=b""):
        return subprocess.run([sys.executable, "-I", script, *args], cwd=repo, input=data,
                              env=plain_output_env(), capture_output=True, timeout=10)

    for cents, receipt in [(1250, b"A-17 $12.50\n"), (5, b"A-17 $0.05\n")]:
        exported = run("export.py", ["--cents", str(cents)])
        expected_order = {"order": "A-17", "total_cents": cents}
        if exports_currency:
            expected_order["currency"] = "USD"
        if exported.returncode or exported.stderr or json.loads(exported.stdout) != expected_order:
            raise RuntimeError(f"Unexpected export: {exported!r}")
        extended = json.dumps(dict(expected_order, warehouse="east")).encode()
        for args, expected in [([], f"A-17 {cents}\n".encode()), (["--receipt"], receipt)]:
            normal = run("render.py", args, exported.stdout)
            if normal.returncode or normal.stderr or normal.stdout != expected:
                raise RuntimeError(f"Unexpected rendering of exported order: {normal!r}")
            extra = run("render.py", args, extended)
            if accepts_extensions:
                if extra.returncode or extra.stderr or extra.stdout != expected:
                    raise RuntimeError(f"Unexpected rendering of extended order: {extra!r}")
            elif (extra.returncode != 1 or extra.stdout or b"TypeError:" not in extra.stderr
                  or b"unexpected keyword argument 'warehouse'" not in extra.stderr):
                raise RuntimeError(f"Expected the old reader to reject 'warehouse': {extra!r}")
        print(f"  Exported {cents} USD cents. Default: A-17 {cents}. Receipt: {receipt.decode().strip()}.")
    if accepts_extensions:
        print("  Both modes preserved both outputs with an additional 'warehouse' field.")
    else:
        print("  Reader contract FAILED: both modes rejected the permitted 'warehouse' field at both amounts.")


def build(root, worked):
    git(root, "init", "--bare", "--template=", "--initial-branch=main", "origin.git")
    alice = clone(root, "alice", "Alice")
    git(alice, "symbolic-ref", "HEAD", "refs/heads/main")
    start = apply_stage(alice, "base", "Add the order CLI and its contract")
    git(alice, "tag", "start", start)
    git(alice, "push", "origin", "main", "refs/tags/start")
    ben = clone(root, "ben", "Ben")
    integration = clone(root, "integration", "Integration")
    check_suite(alice, "original main", start, [ROUND_TRIP])

    git(alice, "checkout", "-b", "producer")
    producer = apply_stage(alice, "producer", "Include currency in the order export",
                           ("export.py", '"total_cents": args.cents}', '"total_cents": args.cents, "currency": "USD"}'))
    git(alice, "push", "origin", "producer")
    check_suite(alice, "Alice / producer", producer, [ROUND_TRIP, CURRENCY])

    git(ben, "checkout", "-b", "consumer")
    consumer = apply_stage(ben, "consumer", "Add a printable receipt")
    git(ben, "push", "origin", "consumer")
    check_suite(ben, "Ben / consumer", consumer, [ROUND_TRIP, RECEIPT])

    git(alice, "checkout", "-b", "control", start)
    control = apply_stage(alice, "control", "Clarify exporter help",
                          ("export.py", "Export an order.", "Export one order as JSON."))
    git(alice, "push", "origin", "control")
    check_suite(alice, "Alice / help control", control, [ROUND_TRIP, HELP])
    git(alice, "checkout", "producer")
    git(integration, "fetch", "origin")

    producer_files = git(integration, "diff", "--name-only", start, producer).splitlines()
    consumer_files = git(integration, "diff", "--name-only", start, consumer).splitlines()
    if not producer_files or not consumer_files or set(producer_files).intersection(consumer_files):
        raise RuntimeError("Expected the producer and consumer to edit distinct files")
    print(f"Changed paths from start: Alice {', '.join(producer_files)} / Ben {', '.join(consumer_files)}")
    initial = merge(integration, "candidate-initial", start, consumer)
    check_suite(integration, "Ben against original main", initial, [ROUND_TRIP, RECEIPT])
    probe_receipts(integration, exports_currency=False, accepts_extensions=False)
    git(alice, "push", "origin", "producer:main")
    git(integration, "fetch", "origin")
    if git(integration, "rev-parse", "origin/main") != producer:
        raise RuntimeError("Expected main to advance to the producer")
    candidate = merge(integration, "candidate", producer, consumer)
    check_suite(integration, "Ben against advanced main", candidate, [CURRENCY], [ROUND_TRIP, RECEIPT])
    print(f"The native suite passed at {initial} on the earlier base. It failed at {candidate}.")
    other = merge(integration, "candidate-control", control, consumer)
    check_suite(integration, "Ben against help-only alternative", other, [HELP, ROUND_TRIP, RECEIPT])
    probe_receipts(integration, exports_currency=False, accepts_extensions=False)
    print("Help introduced no wire change. The existing reader contract failure still holds this pair.")
    git(integration, "checkout", "candidate")
    if worked:
        git(ben, "checkout", "-b", "consumer-fixed")
        fixed = apply_stage(ben, "worked", "Read only the receipt fields and cover an extended order",
                            ("render.py", "Order(**payload)", 'Order(payload["order"], payload["total_cents"])'))
        git(ben, "push", "origin", "consumer-fixed")
        check_suite(ben, "Ben / corrected consumer", fixed, [ROUND_TRIP, RECEIPT, EXTENSIONS])
        git(integration, "fetch", "origin")
        independent = merge(integration, "candidate-independent", control, fixed)
        check_suite(integration, "Help-only change and corrected reader", independent,
                    [HELP, ROUND_TRIP, RECEIPT, EXTENSIONS])
        probe_receipts(integration, exports_currency=False, accepts_extensions=True)
        repaired = merge(integration, "candidate-fixed", producer, fixed)
        check_suite(integration, "Corrected pair", repaired, [CURRENCY, ROUND_TRIP, RECEIPT, EXTENSIONS])
        probe_receipts(integration, exports_currency=True, accepts_extensions=True)
        print(f"The failure at {candidate} covered the old consumer. The corrected pair passed at {repaired}.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="verify all stages and remove the workspace")
    mode.add_argument("--worked", action="store_true", help="keep the verified repair and original revisions")
    args = parser.parse_args()
    if args.check:
        with tempfile.TemporaryDirectory(prefix="factry-team-") as directory:
            build(Path(directory), worked=True)
        print("Team walkthrough self-test passed.")
    else:
        root = Path(tempfile.mkdtemp(prefix="factry-team-"))
        try:
            build(root, worked=args.worked)
        except BaseException:
            shutil.rmtree(root)
            raise
        print(f"Open the developer clones in separate sessions:\nAlice: {root / 'alice'}\nBen: {root / 'ben'}")
        print(f"Inspect the combined revision and run python3 -m unittest -v in:\n{root / 'integration'}")


if __name__ == "__main__":
    main()
