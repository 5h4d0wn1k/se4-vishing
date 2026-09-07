# SE4 — Vishing Lab Kit

Educational vishing **lab kit** for AUTHORIZED internal drills: generates
watermarked call scripts, a call-handler practice simulator, and a trainee scoring
rubric. Real-world use is **refused**; everything is synthetic (example.com
personas, RFC-fictional 1-800-555-01xx numbers).

## Features

- **Call Script Generator** — tech-support and callback scenarios, branded
  `AUTHORIZED INTERNAL DRILL`, watermarked `SIMULATION / AUTHORIZED TRAINING ONLY`.
- **Persona Builder** — synthetic caller personas (never real identities).
- **Call-Handler Practice Sim** — canned safe-vs-risky handling verdicts.
- **Scoring Rubric** — 100-point trainee scoring (PASS / REVIEW / FAIL).
- **JSON + TXT artifacts** under `lab-root/reports/`.

## IMPORTANT: Read before use.

Provided **exclusively** for defensive awareness training and authorized security
testing. Using these scripts to conduct real vishing calls is illegal and unethical.

### Authorization Requirements
- Written approval from your organization's security leadership and a formal
  social-engineering scope are required for any simulated exercise.
- Never target individuals who have not consented to participate.
- `--target-org` is locked to `OWN`.

### Anti-Abuse Safeguards
- Every run requires an explicit `--lab-root`.
- Scripts are only generated for internal drills; all content carries drill
  branding and the watermark.
- Synthetic personas and fictional 555-01xx numbers only.
- Requests to remove these safeguards will be refused.

### Legal Framework
- **CFAA (18 U.S.C. § 1030)**, **wire/mail fraud (18 U.S.C. § 1343)**, state
  wiretapping laws, **EU ePrivacy Directive**.

### Prohibited Use
- Real vishing calls against real individuals or organizations.
- Using scripts to obtain credentials, money, or sensitive data.
- Targeting anyone outside an approved training scope.

### No Warranty
Provided "AS IS". Claim free from functionality.

### Responsible Disclosure
Report observed in-the-wild vishing to relevant authorities and affected orgs.

## Live Lab Test Plan

1. `python3 vishing_toolkit.py --lab-root ./lab --demo` → exit 0, script + TXT/JSON
   artifacts written.
2. `python3 vishing_toolkit.py --lab-root ./lab --rubric` → 100/100 PASS demo.
3. `python3 vishing_toolkit.py --lab-root ./lab --demo --scenario callback` → second scenario.
4. Negative: `python3 vishing_toolkit.py --lab-root ./lab --target-org SomeBank` exits non-zero.
5. `python -m unittest discover -s tests` → 10 offline tests pass.

## Metrics

- Scenarios: 2 (tech_support, callback).
- Synthetic personas: 6 names × 4 roles, deterministic per seed.
- Rubric: 7 criteria, 100 points max, grades PASS(≥70) / REVIEW(≥50) / FAIL.
- Handler sim: safe/risky verdicts via signal matching.
- Test count: 10.

## Usage

```bash
python3 vishing_toolkit.py --lab-root ./lab --demo
python3 vishing_toolkit.py --lab-root ./lab --rubric
python3 vishing_toolkit.py --lab-root ./lab --seed 7
```

## License

MIT