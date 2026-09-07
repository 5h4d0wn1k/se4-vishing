#!/usr/bin/env python3
"""Offline unit tests for SE4 Vishing Lab Kit."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vishing_toolkit import (
    LabGuard, GuardError, PersonaBuilder, VishingScriptGenerator,
    CallHandlerSim, ScoringRubric, WATERMARK, DRILL_BRAND,
)


class TestLabGuard(unittest.TestCase):
    def test_requires_lab_root(self):
        with self.assertRaises(GuardError):
            LabGuard(None)

    def test_requires_own(self):
        with self.assertRaises(GuardError):
            LabGuard("/tmp/x", target_org="Acme Corp")


class TestPersona(unittest.TestCase):
    def test_synthetic(self):
        p = PersonaBuilder(seed=1).generate()
        self.assertTrue(p["drill_only"])
        self.assertTrue(p["email"].endswith("@example.com"))
        self.assertTrue(p["phone"].startswith("1-800-555-01"))


class TestScriptGenerator(unittest.TestCase):
    def test_watermarked_script(self):
        g = VishingScriptGenerator(seed=5)
        s = g.generate("tech_support", "Trainee")
        self.assertTrue(s["watermarked"])
        self.assertIn(WATERMARK, s["text"])
        self.assertIn(DRILL_BRAND, s["text"])

    def test_unknown_scenario(self):
        with self.assertRaises(ValueError):
            VishingScriptGenerator().generate("bogus")


class TestHandlerSim(unittest.TestCase):
    def test_safe_practice(self):
        r = CallHandlerSim().play("I refused and offered a callback")
        self.assertEqual(r["bad_signals"], [])

    def test_risky_practice(self):
        r = CallHandlerSim().play("I gave the OTP over the phone")
        self.assertTrue(r["bad_signals"])


class TestScoringRubric(unittest.TestCase):
    def test_full_marks(self):
        ok = {c: True for c in ScoringRubric.CRITERIA}
        r = ScoringRubric().score(ok)
        self.assertEqual(r["grade"], "PASS")
        self.assertEqual(r["total"], r["max"])

    def test_poor_handling(self):
        ok = {c: False for c in ScoringRubric.CRITERIA}
        r = ScoringRubric().score(ok)
        self.assertEqual(r["grade"], "FAIL")


class TestCliOffline(unittest.TestCase):
    def test_demo_exit_zero(self):
        with tempfile.TemporaryDirectory() as td:
            from vishing_toolkit import main
            code = main(["--lab-root", td, "--demo", "--scenario", "callback"])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(os.path.join(td, "reports", "vishing_script.json")))


if __name__ == "__main__":
    unittest.main()