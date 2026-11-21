class InvalidClaimAmountError(Exception):
    """Raised when a claim amount is zero or negative."""
    pass


class PolicyExpiredException(Exception):
    """Raised when a claim is filed against an expired policy."""
    pass
