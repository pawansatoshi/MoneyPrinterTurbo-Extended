"""CLI entry point for Pawan Video Studio."""

from __future__ import annotations

import argparse

from .engine import render


def main() -> None:
    parser = argparse.ArgumentParser(description="Pawan Video Studio renderer")
    parser.add_argument("manifest", help="Path to a Studio project JSON manifest")
    parser.add_argument("--output", required=True, help="Output MP4 path")
    args = parser.parse_args()
    render(args.manifest, args.output)


if __name__ == "__main__":
    main()
