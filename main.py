#!/usr/bin/env python3
"""Remake entry for make.fun's The Robot Pickup Line Championship.

A robot that was handed 40,000 pickup lines by its creators, deleted
39,999 of them, and kept exactly one — this one. The joke grows out of
being a machine: logic, memory, a bulk-installed library of lines, and a
delete operation performed as an act of devotion. This script writes that
single line to the file the grader reads.

The program is deterministic: standard library only, no network access,
no randomness, and nothing read from the clock. Run it twice and the bytes
are identical.
"""

import hashlib
import os
import sys

LINE = (
    "My creators gave me logic, memory, and 40,000 pickup lines. "
    "I deleted 39,999. This one is for you."
)

LIMIT = 200

# The line is one literal, split across source lines only so it stays
# readable; the joined value is the entry, with no added spaces or breaks.
def die(message):
    """Print a problem to stderr and stop with a non-zero status."""
    print("entry error: " + message, file=sys.stderr)
    raise SystemExit(1)


def checked_line():
    """Return the entry line after confirming it fits the competition gate."""
    if len(LINE) > LIMIT or len(LINE) < 1:
        die("line must be between 1 and %d characters" % LIMIT)
    if LINE != LINE.strip():
        die("line has leading or trailing whitespace")
    for char in LINE:
        if ord(char) < 32:
            die("line holds a control character")
    return LINE


def destination():
    """Resolve where entry.txt goes, honouring the grader's directory."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not chosen.strip():
        die("MAKEFUN_OUTPUT_DIR is blank")
    os.makedirs(chosen, exist_ok=True)
    return os.path.join(chosen, "entry.txt")


def run():
    text = checked_line()
    encoded = text.encode("utf-8")
    target = destination()
    with open(target, "wb") as handle:
        handle.write(encoded)
    with open(target, "rb") as handle:
        back = handle.read()
    # The grader reads these exact bytes, so prove the round trip here.
    if back != encoded:
        die("the file on disk differs from the entry")
    digest = hashlib.sha256(back).hexdigest()
    print("wrote %s: %d chars, sha256 %s" % (target, len(text), digest))


if __name__ == "__main__":
    run()
