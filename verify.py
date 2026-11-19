#!/usr/bin/env python3
"""Standalone verification CLI for the news-image-20261119 entry.

Checks the entry without touching it:
  * entry.png exists next to main.py
  * PNG magic bytes and IHDR dimensions are exactly 1024x1024
  * file size is at most 1 MiB
  * sha256 matches the expected value
  * main.py run twice into two different output directories produces
    byte-identical copies of the repo entry.png

Usage:
    python3 verify.py [--verbose] [--json]

Exit status is 0 when every check passes, 1 otherwise.
"""

import argparse
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

EXPECTED_SHA256 = "90c493d451c92672de8490a173cafc6ee3b4db8c33ec31735fd77283ef8dd4dd"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1024 * 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_dimensions(path):
    """Return (width, height) from the IHDR chunk, or None if invalid."""
    with open(path, "rb") as handle:
        header = handle.read(33)
    if len(header) < 33 or header[:8] != PNG_MAGIC:
        return None
    length, chunk_type = struct.unpack(">I4s", header[8:16])
    if chunk_type != b"IHDR" or length != 13:
        return None
    width, height = struct.unpack(">II", header[16:24])
    return width, height


def run_main_once(main_path, verbose):
    """Run main.py once into a fresh temp directory; return output path."""
    tmpdir = tempfile.mkdtemp(prefix="verify-entry-")
    env = {"MAKEFUN_OUTPUT_DIR": tmpdir}
    result = subprocess.run(
        [sys.executable, str(main_path)],
        env=env,
        capture_output=True,
        text=True,
    )
    if verbose:
        print(f"[verbose] main.py exit={result.returncode} "
              f"stdout={result.stdout.strip()!r} "
              f"stderr={result.stderr.strip()!r}")
    if result.returncode != 0:
        raise RuntimeError(f"main.py failed: {result.stderr.strip()}")
    out = Path(tmpdir) / "entry.png"
    if not out.exists():
        raise RuntimeError(f"main.py wrote no entry.png in {tmpdir}")
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Verify the news-image-20261119 entry.")
    parser.add_argument("--verbose", action="store_true",
                        help="print extra detail while checking")
    parser.add_argument("--json", action="store_true",
                        help="print the report as JSON instead of text")
    parser.add_argument("--expect-sha256", default=EXPECTED_SHA256,
                        help="override the expected sha256 of entry.png "
                             "(default: the shipped entry's hash)")
    args = parser.parse_args(argv)

    repo = Path(__file__).resolve().parent
    entry = repo / "entry.png"
    main_py = repo / "main.py"
    expected = args.expect_sha256.lower()
    checks = []

    def record(name, ok, detail=""):
        checks.append({"name": name, "ok": ok, "detail": detail})
        if args.verbose:
            status = "ok" if ok else "FAIL"
            print(f"[verbose] {status}: {name} {detail}")

    record("entry_exists", entry.is_file(),
           str(entry) if entry.is_file() else "entry.png missing")
    record("main_exists", main_py.is_file(),
           str(main_py) if main_py.is_file() else "main.py missing")

    dims = read_png_dimensions(entry) if entry.is_file() else None
    record("png_magic_and_ihdr", dims is not None,
           f"dimensions={dims}" if dims else "not a valid PNG with IHDR")
    record("dimensions_1024x1024", dims == (EXPECTED_WIDTH, EXPECTED_HEIGHT),
           f"got {dims}, want {(EXPECTED_WIDTH, EXPECTED_HEIGHT)}")

    size = entry.stat().st_size if entry.is_file() else -1
    record("size_within_1mib", 0 <= size <= MAX_BYTES,
           f"{size} bytes (limit {MAX_BYTES})")

    digest = sha256_of(entry) if entry.is_file() else ""
    record("sha256_matches", digest == expected,
           f"got {digest}, want {expected}")

    try:
        out_a = run_main_once(main_py, args.verbose)
        out_b = run_main_once(main_py, args.verbose)
        same_a = sha256_of(out_a) == expected
        same_b = sha256_of(out_b) == expected
        record("determinism_run1", same_a,
               f"run1 sha256={sha256_of(out_a)}")
        record("determinism_run2", same_b,
               f"run2 sha256={sha256_of(out_b)}")
    except (OSError, RuntimeError) as exc:
        record("determinism_runs", False, str(exc))

    passed = all(check["ok"] for check in checks)
    report = {
        "entry": "news-image-20261119",
        "passed": passed,
        "checks": checks,
    }
    if args.json:
        print(json.dumps(report, indent=2))
    else:
        for check in checks:
            mark = "PASS" if check["ok"] else "FAIL"
            print(f"[{mark}] {check['name']}: {check['detail']}")
        print("RESULT: PASS" if passed else "RESULT: FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
