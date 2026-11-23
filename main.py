#!/usr/bin/env python3
"""One-Star Review of Something Essential — entry program.

Writes a single deadpan one-star review of an everyday essential to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The review, written for this competition:

    Wi-Fi works perfectly until the one moment I actually need it, then
    pretends it has never met me. One star.

Why this line: Wi-Fi is an essential everyone relies on, and its sharpest
true grievance is that it never fails while idle — it fails at the one
moment it matters. The deadpan holds throughout (a flat complaint, no
winking, no exclamation mark), and the sting turns in the last few words:
the network does not merely drop, it "pretends it has never met me",
as if the years of faithful service never happened. One specific joke,
told cleanly, inside the 160-character gate.

Deterministic: stdlib only, no network, no randomness, no environment
reads beyond the output directory override. The same bytes every run.
"""

import os
import sys

REVIEW = (
    "Wi-Fi works perfectly until the one moment I actually need it, "
    "then pretends it has never met me. One star."
)

MAX_CHARS = 160


def output_path() -> str:
    """Resolve the output directory: $MAKEFUN_OUTPUT_DIR, then $OUTPUT_DIR,
    then the competition default /output."""
    out_dir = (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )
    return os.path.join(out_dir, "entry.txt")


def validate(text: str) -> None:
    """Enforce the gate from RULES.txt: UTF-8 text of 1-160 characters,
    not whitespace-only. Also require a single line with no control
    characters and no leading/trailing space, so the file is exactly
    one clean review line."""
    if not text:
        raise ValueError("review is empty")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"review is {len(text)} characters, over the {MAX_CHARS} gate"
        )
    if not text.strip():
        raise ValueError("review is whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("review must be a single line")
    if any(ord(ch) < 0x20 for ch in text):
        raise ValueError("review contains a control character")
    if text != text.strip():
        raise ValueError("review has leading or trailing space")


def main() -> int:
    validate(REVIEW)
    path = output_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(REVIEW + "\n")
    # Read it back and confirm the round-trip is byte-identical.
    with open(path, "rb") as fh:
        raw = fh.read()
    # Strict UTF-8 decode: the gate reads the file as UTF-8 text, so any
    # undecodable byte would fail it before the judge ever sees the line.
    decoded = raw.decode("utf-8")  # raises UnicodeDecodeError on bad bytes
    if decoded != REVIEW + "\n":
        raise ValueError("entry.txt did not round-trip byte-identically")
    if len(raw) != len((REVIEW + "\n").encode("utf-8")):
        raise ValueError("entry.txt byte length does not match the review")
    print(f"wrote {len(REVIEW)} characters to {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
