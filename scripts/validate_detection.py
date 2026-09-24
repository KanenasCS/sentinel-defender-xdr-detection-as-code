#!/usr/bin/env python3
"""
Lightweight static checks for Microsoft Defender XDR custom-detection Bicep files.

This is not a replacement for:
- `az bicep build`
- Microsoft-side resource validation
- KQL execution in Advanced Hunting
- runtime custom-detection validation
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DETECTION_ROOT = ROOT / "detections"

REQUIRED_TOKENS = [
    "Microsoft.Security/detectionRules@2026-06-01-preview",
    "queryCondition",
    "queryText",
    "schedule",
    "frequency",
    "detectionAction",
    "alertTemplate",
    "severity",
]

EVENT_IDENTITY_COLUMNS = [
    "Timestamp",
    "DeviceId",
    "ReportId",
]

def check_file(path: Path):
    text = path.read_text(encoding="utf-8")
    errors = []

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"missing required token: {token}")

    for column in EVENT_IDENTITY_COLUMNS:
        if column not in text:
            errors.append(f"query does not reference event identity column: {column}")

    id_match = re.search(r"(?m)^\s*id:\s*'([^']+)'\s*$", text)
    if not id_match:
        errors.append("missing stable detection id")
    else:
        detection_id = id_match.group(1)
        if re.search(r"\d{8,}", detection_id):
            errors.append(
                "detection id looks date/version generated; prefer a stable logical id"
            )

    if "status: 'enabled'" not in text and "status: 'disabled'" not in text:
        errors.append("status should be explicitly set to enabled or disabled")

    return errors


def main():
    files = sorted(DETECTION_ROOT.rglob("*.bicep"))
    if not files:
        print("ERROR: no .bicep detection files found")
        return 1

    failed = False

    for path in files:
        rel = path.relative_to(ROOT)
        errors = check_file(path)

        if errors:
            failed = True
            print(f"[FAIL] {rel}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[PASS] {rel}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
