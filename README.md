> **⚠️ EDUCATIONAL USE ONLY — AUTHORIZED TESTING ONLY.**
> This project exists for education, research, and **defense of systems you own
> or hold explicit written authorization to assess**. Unauthorized use is
> prohibited and may be illegal. Read [ETHICS.md](ETHICS.md) and
> [SCOPE.md](SCOPE.md) before use. Use at your own risk; **AS IS**, no warranty.

# SE4 — Vishing Lab Kit

![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)
![GitHub stars](https://img.shields.io/github/stars/5h4d0wn1k/se4-vishing)
![Last commit](https://img.shields.io/github/last-commit/5h4d0wn1k/se4-vishing)
![GitHub issues](https://img.shields.io/github/issues/5h4d0wn1k/se4-vishing)

Educational **vishing (voice-phishing) drill simulator** for authorized security-awareness training — generates watermarked call scripts, a call-handler practice simulator, and a 100-point trainee scoring rubric, all against synthetic personas and RFC-fictional `1-800-555-01xx` numbers.

## Why

Voice phishing is one of the most effective social-engineering vectors against organizations. SE4 exists to build **security-awareness** without touching real targets: every script is branded `AUTHORIZED INTERNAL DRILL`, watermarked `SIMULATION / AUTHORIZED TRAINING ONLY`, and locked to your own org (`--target-org` is forced to `OWN`). Real-world vishing is illegal and refused by design. This lab kit helps security teams run consent-gated awareness drills, practice call-handler responses, and score trainees consistently — no emails sent, no calls placed, no real identities used.

## Features

- **Call Script Generator** — tech-support and callback scenarios, drill-branded and watermarked.
- **Persona Builder** — synthetic caller personas (never real identities), deterministic per seed.
- **Call-Handler Practice Sim** — canned safe-vs-risky handling verdicts.
- **Scoring Rubric** — 7 criteria / 100 points, grades `PASS`(≥70) / `REVIEW`(≥50) / `FAIL`.
- **JSON + TXT artifacts** under `lab-root/reports/`.
- **Anti-abuse safeguards** — explicit `--lab-root` required; safeguard-removal requests refused.

## Quickstart

```bash
# Demo run: writes script JSON/TXT artifacts, exit 0
python3 vishing_toolkit.py --lab-root ./lab --demo

# Rubric demo: 100/100 PASS
python3 vishing_toolkit.py --lab-root ./lab --rubric

# Second scenario (callback)
python3 vishing_toolkit.py --lab-root ./lab --demo --scenario callback

# Determinism check
python3 vishing_toolkit.py --lab-root ./lab --seed 7
```

```bash
# Run the offline test suite (10 tests)
python3 -m unittest discover -s tests -v
```

## Project structure

```
se4-vishing/
├── vishing_toolkit.py  # CLI: script generator, rubric, handler sim
├── tests/              # offline unittest suite (10 tests)
└── ETHICS.md, SCOPE.md # authorized-use & scope rules
```

## Documentation

- [ETHICS.md](ETHICS.md) — authorized-use policy
- [SCOPE.md](SCOPE.md) — drill scope
- [SECURITY.md](SECURITY.md) — security policy
- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution guide

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Requests to weaken the anti-abuse safeguards will be refused.

## License

MIT. See [LICENSE](LICENSE).