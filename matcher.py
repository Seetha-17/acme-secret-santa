import random
from typing import List, Dict, Tuple
from models import Employee

class SecretSantaEngine:
    """Validates and processes random selection mappings under corporate rules."""

    def _init_(self, participants: List[Employee], exclusions: Dict[str, str] = None):
        self.participants = participants
        self.exclusions = exclusions or {}

    def compute_pairings(self, safety_limit: int = 5000) -> List[Tuple[Employee, Employee]]:
        if len(self.participants) < 2:
            raise ValueError("A minimum of 2 valid employees must be present to form pairings.")

        pool = list(self.participants)
        
        for iteration in range(safety_limit):
            random.shuffle(pool)
            if self._verify_derangement(self.participants, pool):
                return list(zip(self.participants, pool))
                
        raise RuntimeError("An impossible combination structure exists under current rules.")

    def _verify_derangement(self, givers: List[Employee], options: List[Employee]) -> bool:
        for giver, selection in zip(givers, options):
            if giver.email == selection.email:
                return False
            if self.exclusions.get(giver.email) == selection.email:
                return False
        return True