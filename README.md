# SE4 — Vishing Toolkit

Educational voice-phishing (vishing) scenario kit focused on defensive awareness and authorized testing.

## Overview

- Generates templated vishing call scripts for social-engineering training scenarios
- Builds attacker personas and backstories for realistic exercise role-play
- Provides a red-flag and reporting training module for defenders
- Includes phone-number and anchor normalization utilities
- Emphasis is on DEFENSIVE and awareness use and authorized testing
- Zero dependencies — pure Python standard library

## Features

- **Call Script Generator**: Three scenarios (tech support, customer service, urgent authority)
- **Persona Builder**: Randomized attacker backstories with consistent names, companies, and roles
- **Defensive Training Module**: Red-flag list and incident-reporting playbook
- **Phone Normalization**: E.164-style normalization and stable training anchors
- **Script to TXT**: Outputs clean, shareable training scripts and handouts

## Installation

No external dependencies required — uses Python standard library only.

```bash
python3 firmware/vishing_toolkit.py
```

## Usage

```python
from firmware.vishing_toolkit import VishingScriptGenerator, PersonaBuilder, DefensiveTraining

persona = PersonaBuilder().generate()
generator = VishingScriptGenerator(persona)
script = generator.generate(scenario_key="tech_support", target="Training Staff")

handout = DefensiveTraining().handout("1-800-555-0199")

# Save to txt
with open("training_script.txt", "w") as f:
    f.write(script)
```

## Example Output

```
============================================================
VISHING TRAINING SCRIPT — Fake Tech Support Call
Attacker persona : Alleged IT Help Desk Agent
Target subject   : J. Anderson
============================================================
Persona: Alex Carter, Senior Support Engineer at TechNova IT

  Step 1: Hello, this is Alex from TechNova IT support. We have
          detected a critical security breach on your account...

  Step 5: I'll send you a remote-support link at alex.carter@...
          Please install and run it now.
```

## IMPORTANT: Read before use.

This toolkit is provided **exclusively** for defensive awareness training and authorized security testing. Using these scripts to conduct real vishing attacks is illegal and unethical.

### Authorization Requirements

You must obtain explicit written approval from your organization's security leadership and be covered by a formal social-engineering testing scope before conducting any simulated vishing exercise. Never target individuals who have not consented to participate in the training program.

### Legal Framework

Unauthorized telephone deception is governed by the **Computer Fraud and Abuse Act (CFAA)** (18 U.S.C. § 1030), **wire and mail fraud statutes (18 U.S.C. § 1343)**, state wiretapping laws, and the **EU ePrivacy Directive**. Real vishing carries serious criminal penalties, including imprisonment and fines.

### Acceptable Use

- Authorized social-engineering awareness training with informed participants
- Red-team engagements with a signed, scoped testing agreement
- Defensive education for employees and security teams
- Academic study of social-engineering defense

### Prohibited Use

- Conducting vishing calls against real individuals or organizations
- Using these scripts to obtain credentials, money, or other sensitive data
- Targeting persons outside an approved training scope
- Any use that violates applicable law or terms of service

### No Warranty

This software is provided "as is" without warranty of any kind. The authors assume no liability for damages arising from use or misuse of this tool.

### Responsible Disclosure

If you observe in-the-wild vishing campaigns, report them to the relevant authorities and the affected organizations through proper channels.

## License

MIT License