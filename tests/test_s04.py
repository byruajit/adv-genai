"""Session 4 checkpoint. Run from the adv-genai folder with:  uv run pytest tests/test_s04.py

The tests read YOUR file: mywork/loan_rules.py
"""
import sys
from pathlib import Path

import pytest

MYWORK = Path(__file__).resolve().parent.parent / "mywork"
sys.path.insert(0, str(MYWORK))


@pytest.fixture(scope="module")
def lr():
    if not (MYWORK / "loan_rules.py").exists():
        pytest.fail("mywork/loan_rules.py not found. Copy starters/s04_loan_rules.py "
                    "to mywork/loan_rules.py first (README, Session 4, step 2).")
    import loan_rules
    return loan_rules


def good_applicant(lr, **overrides):
    defaults = dict(name="Ravi", monthly_income=80000, existing_emi=10000,
                     credit_score=720, requested_emi=15000)
    defaults.update(overrides)
    return lr.Applicant(**defaults)


def test_check_eligibility_accepts_foir_exactly_at_the_limit(lr):
    a = good_applicant(lr, monthly_income=100000, existing_emi=30000, requested_emi=20000)
    assert lr.check_eligibility(a) == "Ravi: approved, FOIR 0.50"


def test_validate_applicant_rejects_bad_income(lr):
    a = good_applicant(lr, monthly_income=0)
    with pytest.raises(lr.InvalidApplicantError):
        lr.validate_applicant(a)


def test_validate_applicant_rejects_out_of_range_score(lr):
    a = good_applicant(lr, credit_score=950)
    with pytest.raises(lr.InvalidApplicantError):
        lr.validate_applicant(a)


def test_foir_computes_the_ratio(lr):
    a = good_applicant(lr, monthly_income=50000, existing_emi=5000, requested_emi=5000)
    assert lr.foir(a) == pytest.approx(0.2)


def test_check_eligibility_approves_a_good_applicant(lr):
    a = good_applicant(lr)
    result = lr.check_eligibility(a)
    assert result == "Ravi: approved, FOIR 0.31"


def test_check_eligibility_rejects_low_credit_score(lr):
    a = good_applicant(lr, credit_score=600)
    with pytest.raises(lr.LoanRejectedError):
        lr.check_eligibility(a)


def test_safe_check_never_raises_on_rejection(lr):
    a = good_applicant(lr, credit_score=600)
    result = lr.safe_check(a)
    assert result == "Rejected: Ravi: credit score 600 below 650"


def test_summarise_counts_each_outcome(lr):
    applicants = [
        good_applicant(lr, name="Ravi"),
        good_applicant(lr, name="Meera", credit_score=600),
        good_applicant(lr, name="Zoya", monthly_income=0),
    ]
    assert lr.summarise(applicants) == {"approved": 1, "rejected": 1, "invalid": 1}
