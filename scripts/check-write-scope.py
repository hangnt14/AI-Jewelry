#!/usr/bin/env python3
"""Best-effort write-scope guardrail for BA-kit command outputs."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ALLOWED_SUFFIXES = {
    "srs": (
        "/screens/",
        "/usecases/",
        "/data/",
        "/flows/",
        "/srs-groups/",
        "/srs-index.md",
        "/srs.md",
        "/srs-compile-receipt.json",
        "/screen-field-contract.yaml",
    ),
    "wireframes": (
        "/wireframes/",
        "/tool-lanes/tool-lane-state.md",
        "/tool-lanes/figma-make/",
        "/05_tool-lanes/figma-make/",
    ),
    "figma-sync": (
        "/figma-sync/figma-sync-report.md",
        "/figma-sync/figma-mismatch-report.md",
    ),
    "package": (
        "/04_compiled/",
        "/package-snapshot.md",
    ),
}

FORBIDDEN_BY_COMMAND = {
    "figma-sync": (
        "/srs.md",
        "/screens/",
        "/usecases/",
        "/shared-shell-contract.md",
    ),
    "package": (
        "/screens/",
        "/usecases/",
        "/shared-shell-contract.md",
    ),
}


def normalized(path: Path) -> str:
    return "/" + path.as_posix().lstrip("./")


def validate(command: str, paths: list[Path]) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    allowed = ALLOWED_SUFFIXES.get(command)
    forbidden = FORBIDDEN_BY_COMMAND.get(command, ())

    if allowed is None:
        warnings.append(f"unknown command; no write-scope matrix entry: {command}")
        allowed = ()

    for path in paths:
        value = normalized(path)
        if any(token in value for token in forbidden):
            errors.append(f"{path}: forbidden write for command {command}")
            continue
        if allowed and not any(token in value for token in allowed):
            errors.append(f"{path}: outside allowed write scope for command {command}")

    return {"command": command, "errors": errors, "warnings": warnings, "ok": not errors}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True)
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = validate(args.command, args.paths)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(("PASS" if result["ok"] else "BLOCK") + f": {args.command}")
        for error in result["errors"]:
            print(f"BLOCK: {error}")
        for warning in result["warnings"]:
            print(f"WARN: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
