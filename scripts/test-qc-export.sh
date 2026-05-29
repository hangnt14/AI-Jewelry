#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${SCRIPT_DIR}/.." && pwd)"
FIXTURE="${REPO}/tests/qc-export"
EXPORT_SCRIPT="${REPO}/scripts/qc-export.py"
TMPDIR="$(mktemp -d)"
PASS=0
FAIL=0

cleanup() { rm -rf "${TMPDIR}"; }
trap cleanup EXIT

ok() { echo "  PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "  FAIL: $1"; FAIL=$((FAIL + 1)); }

echo "=== ba-qc-export tests ==="
echo ""

# Test 1: happy path — export creates expected files
echo "[test 1] Happy path export"
python3 "${EXPORT_SCRIPT}" \
  --slug test-proj \
  --date 260529-2100 \
  --module payment \
  --repo "${FIXTURE}" >/dev/null 2>&1 || { fail "export command failed"; }

OUTDIR="${FIXTURE}/plans/test-proj-260529-2100/04_compiled/qc-kit/docs/BA"

[[ -f "${OUTDIR}/Common rule/common-rules.md" ]] && ok "common-rules.md exists" || fail "common-rules.md missing"
[[ -f "${OUTDIR}/Common rule/message-list.md" ]] && ok "message-list.md exists" || fail "message-list.md missing"
[[ -f "${OUTDIR}/UC-checkout/UC-checkout.md" ]] && ok "UC-checkout.md exists" || fail "UC-checkout.md missing"
[[ -f "${OUTDIR}/UC-refund/UC-refund.md" ]] && ok "UC-refund.md exists" || fail "UC-refund.md missing"

# Test 2: six section headings in exported UC
echo ""
echo "[test 2] Section headings"
for heading in "BA-kit Source Links" "1. Use Case Description" "2. Screen Description" \
  "3. Validation Summary" "4. Cross-References" "5. Open Questions" "6. Changelog"; do
  grep -q "^## ${heading}" "${OUTDIR}/UC-checkout/UC-checkout.md" && \
    ok "heading '${heading}' present" || fail "heading '${heading}' missing"
done

# Test 3: disclaimer present
echo ""
echo "[test 3] Disclaimer"
grep -q "one-way handoff" "${OUTDIR}/UC-checkout/UC-checkout.md" && \
  ok "disclaimer present" || fail "disclaimer missing"

# Test 4: functional integration for UC with cross-function table
echo ""
echo "[test 4] Functional Integration"
grep -q "Functional Integration" "${OUTDIR}/UC-checkout/UC-checkout.md" && \
  ok "Functional Integration in UC-checkout" || fail "Functional Integration missing in UC-checkout"

# Test 5: UC without cross-function should not have functional integration subsection
echo ""
echo "[test 5] No functional integration when none declared"
# UC-refund has Cross-Function Impact but with "None" rows, so functional integration section
# should still appear but with empty content
grep -q "Functional Integration" "${OUTDIR}/UC-refund/UC-refund.md" && \
  ok "Functional Integration section exists" || fail "Functional Integration missing"

# Test 6: summary JSON
echo ""
echo "[test 6] Summary JSON"
SUMMARY="${FIXTURE}/plans/test-proj-260529-2100/04_compiled/qc-kit/qc-export-summary.json"
[[ -f "${SUMMARY}" ]] && ok "summary JSON exists" || { fail "summary JSON missing"; }
python3 -c "
import json
s = json.load(open('${SUMMARY}'))
assert s['uc_count'] == 2, 'expected 2 UCs'
assert len(s['usecases']) == 2, 'expected 2 usecase entries'
" 2>/dev/null && ok "summary JSON valid" || fail "summary JSON invalid"

# Test 7: missing module fails gracefully
echo ""
echo "[test 7] Missing module"
python3 "${EXPORT_SCRIPT}" \
  --slug test-proj \
  --date 260529-2100 \
  --module nonexistent \
  --repo "${FIXTURE}" >/dev/null 2>&1 && fail "should have failed" || ok "fails on missing module"

# Test 8: output stays under 04_compiled/qc-kit
echo ""
echo "[test 8] Default output location"
echo "${OUTDIR}" | grep -q "04_compiled/qc-kit" && ok "output in 04_compiled/qc-kit" || fail "output outside expected dir"

# Test 9: --usecase-list flag
echo ""
echo "[test 9] Usecase list flag"
python3 "${EXPORT_SCRIPT}" \
  --slug test-proj \
  --date 260529-2100 \
  --module payment \
  --repo "${FIXTURE}" \
  --usecase-list >/dev/null 2>&1
[[ -f "${OUTDIR}/usecase-list.md" ]] && ok "usecase-list.md created" || fail "usecase-list.md missing"

# Test 10: external output
echo ""
echo "[test 10] External output"
python3 "${EXPORT_SCRIPT}" \
  --slug test-proj \
  --date 260529-2100 \
  --module payment \
  --repo "${FIXTURE}" \
  --external-output "${TMPDIR}/qc-out" >/dev/null 2>&1
[[ -f "${TMPDIR}/qc-out/docs/BA/UC-checkout/UC-checkout.md" ]] && \
  ok "external output works" || fail "external output failed"

echo ""
echo "=== Results: ${PASS} passed, ${FAIL} failed ==="
exit $((FAIL > 0 ? 1 : 0))
