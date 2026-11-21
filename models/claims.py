from abc import ABC, abstractmethod
from models.exceptions import InvalidClaimAmountError, PolicyExpiredException


class Claim(ABC):
    def __init__(self, claim_id, customer_name, claim_amount, is_policy_active=True):
        if not is_policy_active:
            raise PolicyExpiredException(f"Policy for {customer_name} is expired.")

        self.__claim_id = claim_id
        self.__customer_name = customer_name
        self.__claim_amount = 0.0
        self.__status = "Pending"
        self.set_claim_amount(claim_amount)

    # Getters
    def get_claim_id(self):
        return self.__claim_id

    def get_customer_name(self):
        return self.__customer_name

    def get_claim_amount(self):
        return self.__claim_amount

    def get_status(self):
        return self.__status

    # Setters with validation
    def set_claim_amount(self, amount):
        if amount <= 0:
            raise InvalidClaimAmountError("Claim amount must be greater than zero.")
        self.__claim_amount = float(amount)

    def set_status(self, status):
        self.__status = status

    @abstractmethod
    def calculate_payout(self):
        pass

    def to_dict(self):
        return {
            "claim_id": self.get_claim_id(),
            "type": self.__class__.__name__,
            "customer_name": self.get_customer_name(),
            "claim_amount": self.get_claim_amount(),
            "payout": self.calculate_payout(),
            "status": self.get_status(),
        }


class HealthClaim(Claim):
    """Covers 80% of the claim after a flat $200 deductible."""
    def calculate_payout(self):
        deductible = 200.0
        net = max(0.0, self.get_claim_amount() - deductible)
        return round(net * 0.80, 2)


class AutoClaim(Claim):
    """Covers 90% of the claim after a flat $500 deductible."""
    def calculate_payout(self):
        deductible = 500.0
        net = max(0.0, self.get_claim_amount() - deductible)
        return round(net * 0.90, 2)


class PropertyClaim(Claim):
    """Covers 85% of the claim after a flat $1000 deductible."""
    def calculate_payout(self):
        deductible = 1000.0
        net = max(0.0, self.get_claim_amount() - deductible)
        return round(net * 0.85, 2)
    