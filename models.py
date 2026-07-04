class Employee:
    """Encapsulates corporate employee identity data and equality structures."""
    
    def _init_(self, name: str, email: str):
        if not name or not name.strip():
            raise ValueError("Employee Name cannot be empty or null.")
        if not email or not email.strip():
            raise ValueError("Employee Email cannot be empty or null.")
            
        self.name = name.strip()
        self.email = email.strip().lower()

    def _eq_(self, other: object) -> bool:
        if not isinstance(other, Employee):
            return False
        return self.email == other.email

    def _hash_(self) -> int:
        return hash(self.email)

    def _repr_(self) -> str:
        return f"Employee({self.name}, {self.email})"