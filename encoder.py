#!/usr/bin/env python3
"""
GP3 Encoder - Reference Implementation
Converts markdown or plain text to GP3 trilingual compressed format.

https://gp3.app/spec | n0v8v LLC | application/vnd.gp3
"""

import argparse
import os
import sys
from pathlib import Path

import anthropic

ENCODE_PROMPT = """You are the GP3 encoder. Convert the input document to GP3 (Glyph-Pipeline-Trilingual) format.

GP3 uses three encoding layers in every K-block:
  L1: CJK ideographs for structural headers and section labels
  L2: English technical terms, identifiers, variable names (never compressed or translated)
  L3: Symbolic operators replacing verbose English logic

Operators:
  → leads_to | ∧ AND | ∨ OR | ∅ NOT/never | ∋ contains | ∈ within_range
  @ triggered_at | {} set | | separator | ↑ escalate | ↓ de-escalate | ≤/≥ comparison

K-block syntax:
  <K{n} id="{CJK_identifier}" load="{trigger}">
    content
  </K{n}>

Load triggers: always | routing | generation | on_{event} | runtime_only | post_exec

Standard block conventions:
  K0 (身份): Identity — name, role, voice, trust boundaries. load=always. Under 200 tokens.
  K1 (路由): Routing — intent classification, priority levels. load=always. Under 200 tokens.
  K2-K3: Domain operational logic. Use domain-specific CJK IDs.
  K4 (能力): Capabilities, tools, integrations.
  K5 (参考): Reference, metrics, feedback loops. load=post_exec.

Rules:
  - Apply all three layers in every K-block
  - Never translate English technical identifiers to CJK
  - No prose inside K-blocks — directives only, one instruction per line
  - Use selective load triggers to keep active context small
  - Target 60-70% token reduction
  - K0 and K1 stay under 200 tokens each

Anti-patterns to avoid:
  - English-only K-blocks with no CJK or operators
  - Prose paragraphs inside K-blocks
  - Overloaded K0 with operational logic (move that to K1+)
  - Every block set to load=always

Output the GP3 file only. No explanation, no preamble, no code fences.

Output format:
# GP3 v1.0 | {document-name}

{K-blocks}

---
n0v8v LLC | GP3 v1.0 | {document-name}.gp3"""


def encode(input_text: str, document_name: str, model: str = "claude-sonnet-4-20250514") -> str:
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=ENCODE_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Document name: {document_name}\n\nEncode this document to GP3:\n\n{input_text}"
            }
        ]
    )
    return message.content[0].text


def token_estimate(text: str) -> int:
    """Rough token estimate: 1 token per 4 characters."""
    return max(1, len(text) // 4)


def print_stats(input_text: str, output_text: str, label: str = "") -> None:
    input_tokens = token_estimate(input_text)
    output_tokens = token_estimate(output_text)
    reduction = (1 - output_tokens / input_tokens) * 100
    prefix = f"[{label}] " if label else ""
    print(f"{prefix}Input:     ~{input_tokens:,} tokens", file=sys.stderr)
    print(f"{prefix}Output:    ~{output_tokens:,} tokens", file=sys.stderr)
    print(f"{prefix}Reduction: {reduction:.1f}%", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GP3 Encoder — Convert markdown to GP3 trilingual compressed format",
        epilog="https://gp3.app/spec | n0v8v LLC"
    )
    parser.add_argument(
        "input",
        help="Input file (.md or .txt), or - to read from stdin"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output path. Defaults to {input}.gp3.md"
    )
    parser.add_argument(
        "-n", "--name",
        help="Document name for the GP3 header. Defaults to input filename stem."
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print token count and compression stats"
    )
    parser.add_argument(
        "--model",
        default="claude-sonnet-4-20250514",
        help="Anthropic model to use (default: claude-sonnet-4-20250514)"
    )

    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    # Read input
    if args.input == "-":
        input_text = sys.stdin.read()
        doc_name = args.name or "document"
        output_path = Path(args.output) if args.output else Path(f"{doc_name}.gp3.md")
    else:
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"Error: {args.input} not found.", file=sys.stderr)
            sys.exit(1)
        input_text = input_path.read_text(encoding="utf-8")
        doc_name = args.name or input_path.stem
        output_path = Path(args.output) if args.output else input_path.with_suffix(".gp3.md")

    if not input_text.strip():
        print("Error: Input is empty.", file=sys.stderr)
        sys.exit(1)

    # Encode
    print(f"Encoding '{doc_name}'...", file=sys.stderr)
    try:
        gp3_output = encode(input_text, doc_name, model=args.model)
    except anthropic.APIError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)

    # Write output
    output_path.write_text(gp3_output, encoding="utf-8")

    if args.stats:
        print_stats(input_text, gp3_output, label=doc_name)

    print(f"Written: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
