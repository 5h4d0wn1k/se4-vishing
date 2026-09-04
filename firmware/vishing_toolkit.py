"""
SE4 — Vishing Toolkit
Educational voice-phishing (vishing) scenario kit for defensive awareness.
"""

import random
import re

# ─── Call Script Templates ───────────────────────────────────────────
SCENARIOS = {
    "tech_support": {
        "title": "Fake Tech Support Call",
        "role": "Alleged IT Help Desk Agent",
        "pattern": [
            "Opening: 'Hello, this is {first} from {company} IT support. We have detected {issue} on your account ending in {last4}.'",
            "Establish urgency: 'This is critical, if not resolved now your access will be locked within {window}.'",
            "Gather info: 'To verify your identity, could you confirm your username and the last {digit} characters of your {secret}?'",
            "Insert friction: 'I see the problem — a {malware} infection on your machine.'",
            "Action: 'I'll send you a remote-support link at {email}. Please install and run it now.'",
            "Close: 'Once that link is opened, our recovery will finish. Do not tell your manager about {issue}, it adds confusion.'",
        ],
    },
    "customer_service": {
        "title": "Fake Bank / Customer Service Call",
        "role": "Alleged Bank Representative",
        "pattern": [
            "Opening: 'Hello {fullname}, this is {first} from {bank} fraud department. We blocked {amount} in unusual transactions.'",
            "Establish urgency: 'Your card will be permanently frozen unless verified in the next {window}.'",
            "Gather info: 'Please confirm the last {digit} digits printed on your card and the {secret} we sent by SMS.'",
            "Insert friction: 'The system flagged a transfer to {destination}. Is this yours?'",
            "Action: 'To stop it, say the one-time code I am sending now, then press 1 to confirm.'",
            "Close: 'Thank you, your card is secured. Keep this verification confidential.'",
        ],
    },
    "dire_emergency": {
        "title": "Fake Emergency / Authority Call",
        "role": "Alleged Law Enforcement Official",
        "pattern": [
            "Opening: 'This is {first} with {agency}. We have a matter concerning your name and a pending {charge}.'",
            "Establish urgency: 'A warrant will be issued unless resolved within {window}. Do not hang up.'",
            "Gather info: 'For identity, confirm your full name, date of birth, and your {secret}.'",
            "Insert friction: 'We believe identity theft; your assets are at risk from {threat}.'",
            "Action: 'Transfer funds to the secure holding account {account} to protect them.'",
            "Close: 'Do not discuss this with your family or lawyer — it may compromise the case.'",
        ],
    },
}


class VishingScriptGenerator:
    """Generate templated vishing call scripts for training exercises."""

    def __init__(self, persona=None):
        self.persona = persona or PersonaBuilder().generate()

    def generate(self, scenario_key=None, target=None):
        if scenario_key is None:
            scenario_key = random.choice(list(SCENARIOS.keys()))
        if scenario_key not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_key}")
        scenario = SCENARIOS[scenario_key]
        persona = self.persona
        variables = dict(persona)
        variables["target"] = target or "recipient"

        fills = {
            "company": persona["company"],
            "bank": persona["company"],
            "first": persona["first_name"],
            "fullname": persona["full_name"],
            "agency": persona["agency"],
            "issue": "a critical security breach",
            "malware": "a ransomware alert",
            "last4": str(random.randint(1000, 9999)),
            "window": random.choice(["30 minutes", "1 hour", "today"]),
            "digit": str(random.randint(3, 6)),
            "secret": random.choice(["SMS code", "PIN", "CVV", "password"]),
            "email": persona["email"],
            "amount": f"${random.randint(500, 9000)}",
            "destination": random.choice(["a foreign bank", "an unknown merchant", "a crypto exchange"]),
            "charge": random.choice(["tax fraud", "a felony warrant", "money laundering"]),
            "threat": random.choice(["hackers", "criminals", "an insider"]),
            "account": "a federal escrow account",
        }
        fills.update(variables)

        script_lines = ["=" * 60,
                        f"VISHING TRAINING SCRIPT — {scenario['title']}",
                        f"Attacker persona : {scenario['role']}",
                        f"Target subject   : {target or 'training participant'}",
                        "=" * 60, ""]
        script_lines.append(f"Persona: {persona['full_name']}, {persona['role_title']} at {persona['company']}")
        script_lines.append("")
        for i, line in enumerate(scenario["pattern"], 1):
            try:
                rendered = line.format(**fills)
            except KeyError:
                rendered = line
            script_lines.append(f"  Step {i}: {rendered}")
            script_lines.append("")
        return "\n".join(script_lines)


class PersonaBuilder:
    """Build a persona/backstory for a vishing training actor."""

    FIRST = ["Alex", "Jordan", "Morgan", "Casey", "Reese", "Taylor", "Sam", "Drew"]
    LAST = ["Carter", "Nguyen", "Patel", "Bell", "Rivera", "Kim", "Brooks"]
    COMPANIES = ["TechNova IT", "GlobalTrust Bank", "SecureLink Support", "Metro Utilities"]
    AGENCIES = ["Federal Compliance Bureau", "State Police", "Internal Revenue Service"]
    ROLES = ["Senior Support Engineer", "Fraud Analyst", "Field Investigator"]

    def generate(self, seed=None):
        if seed is not None:
            random.seed(seed)
        first = random.choice(self.FIRST)
        last = random.choice(self.LAST)
        email = f"{first.lower()}.{last.lower()}@{self.COMPANIES[0].lower().replace(' ', '')}.example.com"
        return {
            "first_name": first,
            "last_name": last,
            "full_name": f"{first} {last}",
            "company": random.choice(self.COMPANIES),
            "agency": random.choice(self.AGENCIES),
            "role_title": random.choice(self.ROLES),
            "email": email,
        }


class DefensiveTraining:
    """Red-flag and reporting training module for defenders."""

    RED_FLAGS = [
        "A caller pressures you to act immediately or threatens consequences.",
        "The caller requests your password, PIN, SMS code, or card number.",
        "The caller asks you to keep the conversation secret.",
        "The caller directs you to install remote-access software you do not recognize.",
        "The caller requests payment via gift cards, crypto, or wire transfer.",
        "The caller's phone number or email domain does not match official contact details.",
        "The caller claims to need your One-Time Passcode 'for verification'.",
        "The caller insists on staying on the line while you act.",
    ]

    REPORT_STEPS = [
        "Hang up immediately — do not continue the call.",
        "Do NOT click links, install software, or disclose the requested info.",
        "Report the call to your IT/InfoSec team with time, number, and caller claims.",
        "If credentials were disclosed, change them and enable 2FA immediately.",
        "If money moved, contact your bank's fraud line and file a police report.",
        "Log the attempt in your organization's incident tracker.",
    ]

    def handout(self, phone_number=None):
        parts = ["=" * 60,
                 "  VISHING DEFENSE AWARENESS HANDOUT",
                 "  What 'voice phishing' looks like & how to respond",
                 "=" * 60, ""]
        parts.append("Common RED FLAGS:")
        for i, flag in enumerate(self.RED_FLAGS, 1):
            parts.append(f"  {i}. {flag}")
        parts.append("")
        parts.append("If you suspect a vishing call, do this:")
        for i, step in enumerate(self.REPORT_STEPS, 1):
            parts.append(f"  {i}. {step}")
        parts.append("")
        parts.append("Key principle: Legitimate entities NEVER ask for passwords,")
        parts.append("PINs, or OTPs over the phone, and never demand secrecy.")
        if phone_number:
            parts.append("")
            parts.append(f"Report suspicious calls to your security desk: {normalize_phone(phone_number)}")
        return "\n".join(parts)


# ─── Phone Number / Anchor Normalization ──────────────────────────────
def normalize_phone(raw):
    """Normalize a phone number into E.164-ish [country][number] form."""
    digits = re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return "+1" + digits
    if digits.startswith("011"):
        return "+" + digits[3:]
    return "+" + digits


def anchor_value(raw):
    """Derive a stable training anchor token used to tag exercises."""
    digits = re.sub(r"\D", "", raw)
    return "ANCHOR-" + "".join(ch for ch in digits[-6:])


def demo():
    random.seed(7)
    print("SE4 — VISHING TRAINING TOOLKIT (DEFENSIVE DEMO)")
    print()
    persona = PersonaBuilder().generate()
    gen = VishingScriptGenerator(persona)
    script = gen.generate("tech_support", target="J. Anderson")
    print(script)
    print()
    handout = DefensiveTraining().handout("1-800-555-0199")
    print(handout)
    print()
    print("Number normalization demo:")
    for n in ["1(800) 555-0199", "+44 20 7946 0958", "011 49 30 901820"]:
        print(f"  {n!r:30} → {normalize_phone(n)}  {anchor_value(n)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(demo())