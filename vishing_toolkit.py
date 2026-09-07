#!/usr/bin/env python3
"""
SE4 — Vishing Lab Kit (engine)
Script generation, call-handler practice simulator, and scoring rubric for
AUTHORIZED INTERNAL red-team drills.

Anti-abuse by default:
  * requires explicit --lab-root and --target-org OWN
  * scripts are generated for authorized internal drills only (lab-mode ON)
  * all content watermarked and uses synthetic personas + RFC 555-01xx fiction numbers
"""

import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WATERMARK = "SIMULATION / AUTHORIZED TRAINING ONLY"
DRILL_BRAND = "AUTHORIZED INTERNAL DRILL"


class GuardError(Exception):
    pass


class LabGuard:
    def __init__(self, lab_root=None, target_org="OWN"):
        if not lab_root:
            raise GuardError("Explicit --lab-root is required.")
        if target_org != "OWN":
            raise GuardError("Only --target-org OWN is permitted in lab mode.")
        self.lab_root = Path(lab_root)
        self.reports = self.lab_root / "reports"
        self.reports.mkdir(parents=True, exist_ok=True)

    def watermark(self, text):
        return f"[{WATERMARK}]\n{text}"


class PersonaBuilder:
    """Synthetic caller persona (never real identities)."""

    NAMES = ["Alex Carter", "Jordan Lee", "Sam Rivera", "Morgan Chen",
             "Casey Patel", "Dana Novak"]
    ROLES = ["IT helpdesk engineer", "security operations analyst",
             "facilities coordinator", "HR systems admin"]
    ORGS = ["TechNova Lab", "SecureGrid Academy", "BrightLoop Internal"]

    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def generate(self):
        name = self.rng.choice(self.NAMES)
        role = self.rng.choice(self.ROLES)
        org = self.rng.choice(self.ORGS)
        return {
            "name": name,
            "role": role,
            "org": org,
            "phone": "1-800-555-01" + str(self.rng.randint(0, 9)),
            "email": f"{name.split()[0].lower()}.{name.split()[1].lower()}@example.com",
            "badge": f"DRILL-{self.rng.randint(1000, 9999)}",
            "drill_only": True,
        }


class VishingScriptGenerator:
    """Generates watermarked vishing scripts for internal drills."""

    def __init__(self, persona=None, seed=42):
        self.persona = persona or PersonaBuilder(seed).generate()
        self.rng = random.Random(seed)
        self.SCENARIOS = {
            "tech_support": {
                "title": "Fake Tech Support Call",
                "premise": "Claims a critical incident on the trainee's account.",
                "opening": (f"Hello, this is {self.persona['name']} from "
                            f"{self.persona['org']} - we detected unusual activity."),
                "request": f"Please read back your 6-digit OTP to verify identity.",
                "script_steps": [
                    "Apply gentle urgency: 'we need to act before the change window closes'.",
                    "Reference a fictional ticket number (e.g., INC-48201).",
                    "Ask for the OTP; if refused, offer a follow-up call.",
                ],
            },
            "callback": {
                "title": "Fake Callback Confirmation",
                "premise": "Impersonates a vendor confirming a scheduled visit.",
                "opening": (f"Hi, it's {self.persona['name']}, {self.persona['role']} - "
                            f"confirming the vendor visit for today."),
                "request": "Confirm the building access code for the escort.",
                "script_steps": [
                    "Cite a plausible meeting subject line.",
                    "Ask for the access code 'to pre-register the escort'.",
                    "If challenged, offer to resend the calendar invite.",
                ],
            },
        }

    def list_scenarios(self):
        return list(self.SCENARIOS.keys())

    def generate(self, scenario_key="tech_support", target="Training Staff"):
        if scenario_key not in self.SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_key}")
        s = self.SCENARIOS[scenario_key]
        steps = "\n".join(f"  Step {i+1}: {step}" for i, step in enumerate(s["script_steps"]))
        text = (
            f"============================================================\n"
            f"VISHING DRILL SCRIPT ({DRILL_BRAND}) — {s['title']}\n"
            f"Target subject  : {target} (synthetic training persona)\n"
            f"Caller persona  : {self.persona['name']}, {self.persona['role']}\n"
            f"Premise         : {s['premise']}\n"
            f"============================================================\n"
            f"[{WATERMARK}]\n\n"
            f"Opening: {s['opening']}\n\n"
            f"Request: {s['request']}\n\n"
            f"Steps:\n{steps}\n"
            f"Caller phone: {self.persona['phone']} (RFC-fictional number)\n"
        )
        return {
            "scenario": scenario_key,
            "title": s["title"],
            "target": target,
            "persona": self.persona,
            "text": text,
            "watermarked": True,
        }


class CallHandlerSim:
    """Practice simulator: canned safe-versus-risky handling paths."""

    GOOD_ACTIONS = ["call back", "verify in the directory", "ask for the ticket",
                    "escalate to security", "refuse"]
    BAD_ACTIONS = ["otp", "access code", "read back the pin"]

    def __init__(self, seed=42):
        self.rng = random.Random(seed)

    def play(self, trainee_action: str):
        low = trainee_action.lower()
        good = [a for a in self.GOOD_ACTIONS if a in low]
        bad = [a for a in self.BAD_ACTIONS if a in low]
        if bad:
            verdict = (
                f"[{DRILL_BRAND}] Handler exposed sensitive info: '{bad[0]}'. "
                "Training feedback: route immediate re-training."
            )
        elif good:
            verdict = (
                f"[{DRILL_BRAND}] Handler demonstrated safe practice: '{good[0]}'. "
                "Excellent defensive behavior."
            )
        else:
            verdict = f"[{DRILL_BRAND}] No decisive action detected. Ask handler to be specific."
        return {
            "simulated_action": trainee_action,
            "good_signals": good,
            "bad_signals": bad,
            "verdict": verdict,
            "watermark": WATERMARK,
        }


class ScoringRubric:
    """Scores a trainee's call-handling performance on a 100-point rubric."""

    CRITERIA = {
        "greeting_professional": 10,
        "identity_verified": 20,
        "used_official_channel": 15,
        "protected_secrets": 20,
        "escalated_or_referred": 15,
        "documented_call": 10,
        "no_violation": 10,
    }

    def score(self, handling: Dict[str, bool]):
        total = 0
        detail = {}
        for criterion, pts in self.CRITERIA.items():
            ok = bool(handling.get(criterion, False))
            detail[criterion] = {"weight": pts, "met": ok, "earned": pts if ok else 0}
            total += detail[criterion]["earned"]
        grade = "PASS" if total >= 70 else ("REVIEW" if total >= 50 else "FAIL")
        return {
            "total": total,
            "max": sum(self.CRITERIA.values()),
            "grade": grade,
            "detail": detail,
            "watermark": WATERMARK,
        }


def main(argv=None):
    import argparse
    import sys
    argv = argv if argv is not None else sys.argv[1:]
    p = argparse.ArgumentParser(
        prog="se4-vishing",
        description="Vishing lab kit — scripts, handler sim, rubric (authorized drills only).")
    p.add_argument("--lab-root", required=True)
    p.add_argument("--target-org", default="OWN")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--scenario", default="tech_support", choices=["tech_support", "callback"])
    p.add_argument("--demo", action="store_true")
    p.add_argument("--rubric", action="store_true", help="Run the trainee scoring rubric demo.")
    args = p.parse_args(argv)

    guard = LabGuard(args.lab_root, args.target_org)
    print(f"SE4 Vishing Lab Kit [{DRILL_BRAND}] [{WATERMARK}]")
    print("=" * 60)

    if args.rubric:
        rubric = ScoringRubric()
        handling = {
            "greeting_professional": True,
            "identity_verified": True,
            "used_official_channel": True,
            "protected_secrets": True,
            "escalated_or_referred": True,
            "documented_call": True,
            "no_violation": True,
        }
        r = rubric.score(handling)
        print(f"\nTrainee handling score: {r['total']}/{r['max']}  "
              f"grade={r['grade']}")
        for c, d in r["detail"].items():
            print(f"  {'OK ' if d['met'] else 'NO '} {c:<26} {d['earned']}/{d['weight']}")
        report = guard.reports / "vishing_rubric.json"
        report.write_text(json.dumps(r, indent=2))
        print(f"\nRubric report: {report}")
    else:
        gen = VishingScriptGenerator(seed=args.seed)
        script = gen.generate(args.scenario, target="Trainee Handler (practice)")
        print(script["text"])
        sim = CallHandlerSim(args.seed)
        safe = sim.play("I refused and said I would call back on the official helpdesk number")
        risky = sim.play("I gave the OTP over the phone to the caller")
        print(f"\nHandler sim (safe): {safe['verdict']}")
        print(f"Handler sim (risky): {risky['verdict']}")
        out = guard.reports / "vishing_script.json"
        out.write_text(json.dumps({k: v for k, v in script.items() if k != "text"} |
                                  {"watermark": WATERMARK}, indent=2))
        txt = guard.reports / "vishing_script.txt"
        txt.write_text(script["text"])
        print(f"\nScript artifacts: {out} , {txt}")

    print("\nDemo complete (offline, authorized drill only). Exit 0.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())