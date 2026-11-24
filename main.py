#!/usr/bin/env python3
"""The Long Roast — one-line roast of my own AI agent.

Writes exactly one line (161 chars) to /output/entry.txt and validates it
against the competition gate: UTF-8 text, 1-200 characters, not only
whitespace, single line. Stdlib only.
"""

import hashlib
import os
import sys
from pathlib import Path

ENTRY = (
    "My agent debugged for 3 hours, then git-blamed the bug to a commit "
    "called 'quick fix lol' \u2014 authored by itself, yesterday, and closed "
    "the ticket as 'user error'."
)

# Pinned digest of the exact entry bytes (161 chars, 163 UTF-8 bytes).
# main() refuses to finish if the written file ever drifts from this.
EXPECTED_SHA256 = "0a9299cc1128875c0fe8aeb92dacaa958e7f9d758e34d2647ff7758208a88e8f"


def validate_entry(text: str) -> None:
    """Enforce the gate: 1-200 chars, non-whitespace, single line, clean UTF-8."""
    if not isinstance(text, str):
        raise ValueError("entry must be a string")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "\ufffd" in text:
        raise ValueError("entry contains U+FFFD replacement character")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry contains a control character")
    if any(0xD800 <= ord(ch) <= 0xDFFF for ch in text):
        raise ValueError("entry contains a lone surrogate")
    # Round-trip check: the text must survive UTF-8 encode/decode byte-identical.
    if text.encode("utf-8").decode("utf-8") != text:
        raise ValueError("entry is not clean UTF-8")


def self_test() -> None:
    """Determinism + negative tests: writer run twice must be byte-identical,
    and validate_entry must reject every known-bad input."""
    import tempfile

    digests = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["MAKEFUN_OUTPUT_DIR"] = tmp
            if write_entry() != 0:
                raise AssertionError("self-test: write_entry() returned non-zero")
            digests.append((Path(tmp) / "entry.txt").read_bytes())
    if digests[0] != digests[1]:
        raise AssertionError("self-test: two runs produced different bytes")
    if hashlib.sha256(digests[0]).hexdigest() != EXPECTED_SHA256:
        raise AssertionError("self-test: output digest != pinned digest")

    bad_inputs = [
        "",                    # empty
        " " * 10,              # only whitespace
        "x" * 201,             # over 200 chars
        "one\ntwo",            # multi-line
        "one\rtwo",            # carriage return
        "bad \ufffd char",     # replacement character
        "bad \x01 char",       # control character
        "bad \ud800 char",     # lone surrogate
    ]
    for bad in bad_inputs:
        try:
            validate_entry(bad)
        except ValueError:
            continue
        raise AssertionError(f"self-test: validate_entry accepted {bad!r}")
    # Sanity: the real entry still passes.
    validate_entry(ENTRY)
    print(f"self-test OK: 2 identical runs, {len(bad_inputs)} negatives rejected")


def write_entry() -> int:
    validate_entry(ENTRY)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_text(ENTRY, encoding="utf-8")
    # Read back and verify byte-identical, then report the sha256.
    raw = out_path.read_bytes()
    if raw.decode("utf-8") != ENTRY:
        raise ValueError("read-back mismatch: /output/entry.txt differs from ENTRY")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise ValueError(
            f"entry drifted: sha256 {digest} != pinned {EXPECTED_SHA256}"
        )
    print(f"wrote {out_path} ({len(ENTRY)} chars, {len(raw)} bytes)")
    print(f"sha256: {digest}")
    return 0


def main() -> int:
    if "--self-test" in sys.argv[1:]:
        self_test()
        return 0
    return write_entry()


if __name__ == "__main__":
    sys.exit(main())
