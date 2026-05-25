#!/usr/bin/env python3
"""Run lightweight SRS canon guardrails for a module directory."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run_check(cmd: list[str]) -> dict[str, object]:
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    return {
        "cmd": " ".join(cmd),
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("module_root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    module_root = args.module_root
    script_dir = Path(__file__).resolve().parent
    project_root = module_root.parent.parent if module_root.parent.name == "03_modules" else module_root.parent
    shared_index = project_root / "02_backbone" / "shared-rule-message-index.md"
    checks: list[dict[str, object]] = []

    index_path = module_root / "srs-index.md"
    if index_path.exists():
        checks.append(run_check([sys.executable, str(script_dir / "check-srs-index-consistency.py"), str(index_path)]))
    else:
        checks.append({"cmd": "check-srs-index-consistency", "returncode": 1, "stdout": "", "stderr": "missing srs-index.md"})

    for screen in sorted((module_root / "screens").glob("*.md")):
        cmd = [sys.executable, str(script_dir / "check-screen-canon-schema.py"), str(screen)]
        if shared_index.exists():
            cmd.extend(["--shared-index", str(shared_index)])
        checks.append(run_check(cmd))

    compile_receipt = module_root / "srs-compile-receipt.json"
    compiled_srs = module_root / "srs.md"
    receipt_status = "present" if compile_receipt.exists() else "missing"
    if compiled_srs.exists() and not compile_receipt.exists():
        checks.append({"cmd": "compile receipt", "returncode": 1, "stdout": "", "stderr": "compiled srs.md exists but srs-compile-receipt.json is missing"})
    checks.append(run_check([sys.executable, str(script_dir / "check-source-of-truth.py"), str(module_root)]))
    checks.append(run_check([sys.executable, str(script_dir / "validate-shared-rule-message-registry.py"), "--module-root", str(module_root)]))

    ok = all(int(check["returncode"]) == 0 for check in checks)
    result = {"module_root": str(module_root), "ok": ok, "compile_receipt": receipt_status, "checks": checks}

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(("PASS" if ok else "BLOCK") + f": {module_root}")
        for check in checks:
            if check["stdout"]:
                print(check["stdout"])
            if check["stderr"]:
                print(f"BLOCK: {check['stderr']}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
