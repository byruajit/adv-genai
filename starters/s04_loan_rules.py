"""Session 4: loan_rules.py — YOUR file

Picks up where Session 3 left off. clean_text.py cleaned and masked a raw
message; this module decides whether the applicant behind that message
qualifies for a loan. New tools this time: functions with default
arguments, a dataclass to hold the applicant's fields, type hints on every
signature, and two custom exceptions for two different kinds of "no".

Fill in each function body. Run the checkpoint with:
    uv run pytest tests/test_s04.py
"""

from dataclasses import dataclass


class InvalidApplicantError(Exception):
    """The applicant record itself is unusable (bad data, not a credit decision)."""


class LoanRejectedError(Exception):
    """The applicant record is fine, but does not qualify for the loan."""


@dataclass
class Applicant:
    name: str
    monthly_income: float
    existing_emi: float
    credit_score: int
    requested_emi: float


def validate_applicant(a: Applicant, min_credit_score: int = 650) -> None:
    """Raise InvalidApplicantError if the record itself cannot be used.

    This only checks that the numbers make sense (positive income, a score
    in range) — it is not yet asking whether the applicant qualifies.
    """
    pass   # YOU: replace this line


def foir(a: Applicant) -> float:
    """Fixed Obligation to Income Ratio: total EMI load divided by income."""
    pass   # YOU: replace this line


def check_eligibility(a: Applicant, min_credit_score: int = 650, max_foir: float = 0.5) -> str:
    """Validate the record, then decide. Raises LoanRejectedError on a "no"."""
    pass   # YOU: replace this line


def safe_check(a: Applicant) -> str:
    """Never raises. Turns any rejection or bad record into one friendly line."""
    pass   # YOU: replace this line


def summarise(applicants: list[Applicant]) -> dict[str, int]:
    """Count how many applicants in the list were approved, rejected, or invalid."""
    pass   # YOU: replace this line


APPLICANTS = [
    Applicant("Ravi", monthly_income=80000, existing_emi=10000, credit_score=720, requested_emi=15000),
    Applicant("Meera", monthly_income=40000, existing_emi=5000, credit_score=600, requested_emi=20000),
    Applicant("Zoya", monthly_income=0, existing_emi=0, credit_score=700, requested_emi=10000),
]

if __name__ == "__main__":
    for applicant in APPLICANTS:
        print(safe_check(applicant))
    print(summarise(APPLICANTS))
