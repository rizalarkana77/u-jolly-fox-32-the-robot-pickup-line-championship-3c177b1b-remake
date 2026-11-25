#!/usr/bin/env python3
"""Robot pickup line, remake entry for make.fun.

The setup: the robot's creators installed logic, memory, and forty
thousand pickup lines. The robot kept one line and deleted the other
39,999. That deletion is the flirtation — a machine treating a bulk
library as clutter and a single kept line as the point. This is a
remake: the first line entered for this competition ranked 1573/2218
in round 1, outside the top 10, so this is a new line on a different
machine joke — a library and a delete key, not a cooling fan.

This module validates the line against the competition gate (one line,
1 to 200 characters, no control characters, no surrounding whitespace)
and writes it to entry.txt where the grader looks for it. Everything
is standard library, deterministic, offline, and clock-free: the same
input always produces the same bytes.
"""

import hashlib
import os
import sys

ENTRY = "My creators gave me logic, memory, and 40,000 pickup lines. I deleted 39,999. This one is for you."
MAX_CHARS = 200


def fail(reason):
    sys.stderr.write("entry error: %s\n" % reason)
    raise SystemExit(1)


def validate(line):
    if not 1 <= len(line) <= MAX_CHARS:
        fail("line must be 1 to %d characters, got %d" % (MAX_CHARS, len(line)))
    if line.strip() != line:
        fail("line has leading or trailing whitespace")
    bad = [c for c in line if ord(c) < 32]
    if bad:
        fail("line holds %d control character(s)" % len(bad))
    if "\n" in line or "\r" in line:
        fail("line must be a single line")
    return line


def output_path():
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if not directory.strip():
        fail("MAKEFUN_OUTPUT_DIR is blank")
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, "entry.txt")


def main():
    line = validate(ENTRY)
    payload = line.encode("utf-8")
    target = output_path()
    with open(target, "wb") as stream:
        stream.write(payload)
    with open(target, "rb") as stream:
        stored = stream.read()
    if stored != payload:
        fail("the file on disk differs from the entry")
    digest = hashlib.sha256(stored).hexdigest()
    sys.stdout.write(
        "wrote %s: %d chars, sha256 %s\n" % (target, len(line), digest)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
