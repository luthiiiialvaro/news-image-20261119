# news-image-20261119: one image that sums up 19 November 2026
#
# A make.fun entry (Python 3.13, standard library only). The image the
# program writes is the entry.png beside this file: a newspaper front
# page drawn for Thursday 19 November 2026, with the day's six biggest
# stories and a ticker of five more. The program copies it to
# /output/entry.png, so both graded runs write the same bytes.
#
# Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
# /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
#   python3 main.py --help

import hashlib
import os
import shutil
import struct
import sys

# The gate takes a whole PNG of at most 1 MiB and 1024 by 1024 pixels.
MAX_BYTES = 1048576
MAX_SIDE = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"

USAGE = """usage: python3 main.py [--help]

Copy entry.png (1024x1024, at most 1 MiB) to the output directory and
verify the copy is byte-identical.

  /output/entry.png            inside the grader's container
  $MAKEFUN_OUTPUT_DIR/entry.png  anywhere else (defaults to /output)

Exit status is 0 on success, 1 when the image fails a gate check or the
copy cannot be written."""


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_png_size(path):
    """Return (width, height) from a PNG header, or None if not a PNG."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        return None
    # After the 8-byte magic comes the 25-byte IHDR chunk: length (4),
    # type "IHDR" (4), width (4, big-endian), height (4, big-endian).
    if head[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main(argv):
    if "--help" in argv or "-h" in argv:
        print(USAGE)
        return 0
    for arg in argv[1:]:
        print("unknown argument: %s" % arg, file=sys.stderr)
        print(USAGE, file=sys.stderr)
        return 1

    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    # In the grader's container the output directory is /output; outside
    # it, MAKEFUN_OUTPUT_DIR stands in for it (see the header comment).
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(source):
        print("entry.png is missing next to main.py (%s)" % source,
              file=sys.stderr)
        return 1
    size = read_png_size(source)
    if size is None:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1
    width, height = size
    if width > MAX_SIDE or height > MAX_SIDE:
        print("entry.png is %dx%d, over 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print("entry.png is over 1 MiB", file=sys.stderr)
        return 1

    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError as exc:
        print("cannot create output directory %s: %s" % (out_dir, exc),
              file=sys.stderr)
        return 1
    if not os.access(out_dir, os.W_OK):
        print("output directory %s is not writable" % out_dir,
              file=sys.stderr)
        return 1
    try:
        shutil.copyfile(source, target)
    except OSError as exc:
        print("cannot write %s: %s" % (target, exc), file=sys.stderr)
        return 1
    # The two graded runs must write the same bytes: confirm the copy is
    # byte-identical to the source before reporting success.
    source_hash = _sha256(source)
    if source_hash != _sha256(target):
        print("copy mismatch: %s differs from %s" % (target, source),
              file=sys.stderr)
        return 1
    target_size = os.path.getsize(target)
    if target_size > MAX_BYTES:
        print("copied file is %d bytes, over 1 MiB" % target_size,
              file=sys.stderr)
        return 1
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (target, width, height, target_size, source_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
