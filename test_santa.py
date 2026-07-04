import unittest
from models import Employee
from matcher import SecretSantaEngine

class VerificationTestSuite(unittest.TestCase):
    
    def setUp(self):
        self.staff_a = Employee("Hamish Murray", "hamish.murray@acme.com")
        self.staff_b = Employee("Layla Graham", "layla.graham@acme.com")
        self.staff_c = Employee("Matthew King", "matthew.king@acme.com")
        self.team = [self.staff_a, self.staff_b, self.staff_c]

    def test_prevention_of_self_matching(self):
        engine = SecretSantaEngine(self.team)
        results = engine.compute_pairings()
        for internal_giver, assigned_child in results:
            self.assertNotEqual(internal_giver.email, assigned_child.email)

    def test_strict_historical_exclusion_rules(self):
        prior_rules = {"hamish.murray@acme.com": "layla.graham@acme.com"}
        engine = SecretSantaEngine(self.team, prior_rules)
        results = engine.compute_pairings()
        
        for internal_giver, assigned_child in results:
            if internal_giver.email == "hamish.murray@acme.com":
                self.assertNotEqual(assigned_child.email, "layla.graham@acme.com")

    def test_boundary_limits_for_single_inputs(self):
        engine = SecretSantaEngine([self.staff_a])
        with self.assertRaises(ValueError):
            engine.compute_pairings()

if _name_ == '_main_':
    unittest.main()