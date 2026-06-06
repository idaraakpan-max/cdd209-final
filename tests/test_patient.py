import pandas as pd
import pytest

from pharma_adherence.patient import PatientAdherenceProfile

"""
RUN THIS SCRIPT USING `PYTHONPATH=src pytest -v`
"""

def make_patient_df():
    return pd.DataFrame(
        {
            "fill_date": pd.to_datetime(["2025-03-02", "2024-12-30", "2025-01-26"]),
            "copay_amount": [12.60, 19.73, 9.00],
            "days_supply": [30, 60, 60],
            "proportion_days_covered": [0.65, 0.57, 0.78],
        }
    )


def test_init_sorts_by_fill_date():
    df = make_patient_df()

    profile = PatientAdherenceProfile("P001", df)

    assert list(profile.df["fill_date"]) == list(pd.to_datetime(["2024-12-30", "2025-01-26", "2025-03-02"]))


def test_total_fills():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.total_fills() == 3


def test_average_copay():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.average_copay() == pytest.approx((19.73 + 9.00 + 12.60) / 3)


def test_average_days_supply():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.average_days_supply() == pytest.approx((60 + 60 + 30) / 3)


def test_calculate_pdc():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.calculate_pdc() == pytest.approx((0.57 + 0.78 + 0.65) / 3)


def test_is_adherent_default_threshold():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.is_adherent() == False


def test_is_adherent_custom_threshold():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    assert profile.is_adherent(threshold=0.5) == True


def test_summary():
    profile = PatientAdherenceProfile("P001", make_patient_df())

    expected = {
        "patient_id": "P001",
        "total_fills": 3,
        "avg_copay": pytest.approx((19.73 + 9.00 + 12.60) / 3),
        "avg_days_supply": pytest.approx((60 + 60 + 30) / 3),
        "pdc": pytest.approx((0.57 + 0.78 + 0.65) / 3),
        "adherent": False,
    }

    result = profile.summary()

    assert result["patient_id"] == expected["patient_id"]
    assert result["total_fills"] == expected["total_fills"]
    assert result["avg_copay"] == expected["avg_copay"]
    assert result["avg_days_supply"] == expected["avg_days_supply"]
    assert result["pdc"] == expected["pdc"]
    assert result["adherent"] == expected["adherent"]