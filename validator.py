#!/usr/bin/env python3
"""
GP3 Validator - Reference Implementation
Validates GP3 file structure and syntax against the spec.

https://gp3.app/spec | n0v8v LLC | application/vnd.gp3
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

VALID_LOAD_TRIGGERS = {"always", "routing", "generation", "runtime_only", "post_exec"}

CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3400-\u4dbf\u30a0-\u30ff]")
GP3_OPERATORS = ["→", "∧", "∨", "∅", "∋", "∈", "↑", "↓", "≤", "≥", "@"]
HEADER_PATTERN = re.compile(r"^#\s+GP3\s+v[\d.]+\s+\|", re.MULTILINE)
OPEN_TAG_PATTERN = re.compile(r"<(K\d+)\s+([^>]*)>")
CLOSE_TAG_PATTERN = re.compile(r"</(K\d+)>")
ID_ATTR_PATTERN = re.compile(r'\bid="([^"]*)"')
LOAD_ATTR_PATTERN = re.compile(r'\bload="([^"]*)"')


@dataclass
class ValidationResult:
    filename: str
    valid: bool = True
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def error(self, msg: str) -> None:
        self.errors.append(msg)
        self.valid = False

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def validate(content: str, filename: str = "<input>") -> ValidationResult:
    r = ValidationResult(filename=filename)

    # Rule 1: Header within first 512 bytes
    first_512 = content[:512]
    if not HEADER_PATTERN.search(first_512):
        r.error(
            "Missing GP3 header. File must contain '# GP3 v{version} | {name}' "
            "within the first 512 bytes."
        )

    # Rule 3+4: K-block structure and required attributes
    open_matches = OPEN_TAG_PATTERN.findall(content)
    close_matches = CLOSE_TAG_PATTERN.findall(content)

    open_tags = [tag for tag, _ in open_matches]
    close_tags = list(close_matches)

    if open_tags != close_tags:
        r.error(
            f"Mismatched K-block tags.\n"
            f"  Opened:  {open_tags}\n"
            f"  Closed:  {close_tags}"
        )

    ids_seen = []
    for tag, attrs in open_matches:
        id_match = ID_ATTR_PATTERN.search(attrs)
        load_match = LOAD_ATTR_PATTERN.search(attrs)

        if not id_match:
            r.error(f"<{tag}> is missing required 'id' attribute.")
        else:
            ids_seen.append(id_match.group(1))

        if not load_match:
            r.error(f"<{tag}> is missing required 'load' attribute.")
        else:
            load_val = load_match.group(1)
            if load_val not in VALID_LOAD_TRIGGERS and not load_val.startswith("on_"):
                r.error(
                    f"<{tag}> has invalid load trigger '{load_val}'. "
                    f"Valid values: {', '.join(sorted(VALID_LOAD_TRIGGERS))}, or on_{{event}}."
                )

    # Rule 5: Sequential numbering from K0
    if open_tags:
        try:
            numbers = [int(t[1:]) for t in open_tags]
            expected = list(range(len(numbers)))
            if numbers != expected:
                r.error(
                    f"K-blocks must be numbered sequentially from K0. "
                    f"Found: {open_tags}"
                )
        except ValueError:
            r.error("Could not parse K-block numbering.")

    # Rule 6: Unique IDs
    if len(ids_seen) != len(set(ids_seen)):
        dupes = [i for i in ids_seen if ids_seen.count(i) > 1]
        r.error(f"Duplicate K-block id values: {list(set(dupes))}")

    # Warnings
    if not open_tags:
        r.warn("No K-blocks found. A valid GP3 file needs at least K0.")

    if not CJK_PATTERN.search(content):
        r.warn(
            "No CJK characters found. GP3 requires Layer 1 (CJK) structural headers."
        )

    if not any(op in content for op in GP3_OPERATORS):
        r.warn(
            "No GP3 operators found. GP3 requires Layer 3 (symbolic) operators."
        )

    # K0/K1 always-loaded blocks: rough token warning
    for tag, attrs in open_matches:
        load_match = LOAD_ATTR_PATTERN.search(attrs)
        if load_match and load_match.group(1) == "always":
            # Extract block content
            block_pattern = re.compile(
                rf"<{tag}[^>]*>(.*?)</{tag}>", re.DOTALL
            )
            block_match = block_pattern.search(content)
            if block_match:
                block_content = block_match.group(1)
                estimated_tokens = max(1, len(block_content) // 4)
                if estimated_tokens > 200:
                    r.warn(
                        f"<{tag}> (load=always) is ~{estimated_tokens} tokens. "
                        f"Recommended: under 200 tokens for always-loaded blocks."
                    )

    return r


def print_result(result: ValidationResult, verbose: bool = True) -> None:
    status = "PASS" if result.valid else "FAIL"
    print(f"[{status}] {result.filename}")
    if verbose or not result.valid:
        for err in result.errors:
            print(f"  ERROR: {err}")
        for warn in result.warnings:
            print(f"  WARN:  {warn}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GP3 Validator — Validate GP3 file structure and syntax",
        epilog="https://gp3.app/spec | n0v8v LLC"
    )
    parser.add_argument(
        "files",
        nargs="+",
        help="GP3 file(s) to validate (.gp3 or .gp3.md)"
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output for passing files"
    )

    args = parser.parse_args()
    all_valid = True

    for filepath in args.files:
        path = Path(filepath)
        if not path.exists():
            print(f"[ERROR] {filepath}: file not found")
            all_valid = False
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            print(f"[ERROR] {filepath}: UTF-8 decode failed — {e}")
            all_valid = False
            continue

        result = validate(content, filename=filepath)
        if not result.valid:
            all_valid = False

        if not args.quiet or not result.valid:
            print_result(result, verbose=not args.quiet)

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
