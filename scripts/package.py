"""Build or verify a Factry skills ZIP from an explicit Git revision."""

import argparse
import io
import os
from pathlib import Path
import re
import subprocess
from zipfile import ZIP_STORED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parents[1]
CATALOG = "scripts/skill-catalog.txt"
LEGACY_SKILLS = {
    "factry-address-review", "factry-debug", "factry-fix-ci", "factry-implement",
    "factry-plan", "factry-post-merge", "factry-release", "factry-review",
    "factry-scout", "factry-ship", "factry-verify",
}


def git(*args):
    # Hooks and shell wrappers can export another repository's Git directory or
    # object store. A local replacement object can also shadow a committed blob.
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
    return subprocess.check_output(["git", "--no-replace-objects", *args], cwd=ROOT, env=env)


def catalog_at(commit):
    entry = git("ls-tree", commit, "--", CATALOG)
    if not entry:
        # Releases v0.2.0 through v0.3.0 had a fixed eleven-skill layout.
        return LEGACY_SKILLS
    if not entry.startswith(b"100644 blob "):
        raise ValueError("Expected a regular skill catalog.")
    names = git("show", f"{commit}:{CATALOG}").decode("ascii").splitlines()
    if (not names or names != sorted(set(names)) or
            any(not re.fullmatch(r"factry-[a-z0-9]+(?:-[a-z0-9]+)*", name) for name in names)):
        raise ValueError("Expected sorted, unique skill names in the release catalog.")
    return set(names)


def package_bytes(ref):
    if not ref or ref.startswith("-"):
        raise ValueError("Supply a Git tag, branch, or commit ID.")
    commit = git("rev-parse", "--verify", ref + "^{commit}").decode("ascii").strip()
    skills = catalog_at(commit)
    tree = git("ls-tree", "-r", "-z", commit, "--", "LICENSE", "skills")
    blobs = {}
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, object_id = metadata.split()
        path = raw_path.decode("utf-8")
        parts = path.split("/")
        if (any(part in ("", ".", "..") for part in parts)
                or "\\" in path or ":" in path or not path.isprintable()):
            raise ValueError(f"Unsafe archive path: {path!r}")
        if path != "LICENSE" and not (
                len(parts) >= 3 and parts[0] == "skills" and parts[1] in skills):
            raise ValueError(f"Unexpected package path: {path}")
        if mode not in (b"100644", b"100755") or kind != b"blob":
            raise ValueError(f"Expected a regular Git file: {path}")
        blobs[path] = (object_id.decode("ascii"), int(mode, 8))

    required = {"LICENSE"} | {f"skills/{name}/SKILL.md" for name in skills}
    missing = required.difference(blobs)
    if missing:
        raise ValueError("Missing package files: " + ", ".join(sorted(missing)))
    output = io.BytesIO()
    with ZipFile(output, "w", compression=ZIP_STORED) as archive:
        archive.comment = commit.encode("ascii")
        for path, (object_id, mode) in sorted(blobs.items()):
            entry = ZipInfo(path, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = mode << 16
            archive.writestr(entry, git("cat-file", "blob", object_id))
    return commit, output.getvalue()


def verify(path, expected):
    # Compare the canonical bytes without opening or extracting an untrusted ZIP.
    with path.open("rb") as downloaded:
        if downloaded.read(len(expected) + 1) != expected:
            raise ValueError("Archive differs from the package built from this revision.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("build", "verify"))
    parser.add_argument("ref", help="Git tag, branch, or commit ID")
    parser.add_argument("archive", type=Path, help="local ZIP file (new path for build)")
    args = parser.parse_args()
    try:
        commit, expected = package_bytes(args.ref)
        if args.action == "build":
            with args.archive.open("xb") as output:
                output.write(expected)
        else:
            verify(args.archive, expected)
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"Package {args.action} failed: {exc}\n")
    print(f"Package {args.action} succeeded for {commit}: {args.archive}")


if __name__ == "__main__":
    main()
