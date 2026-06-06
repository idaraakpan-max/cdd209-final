import pandas as pd
import numpy as np


def _clean_text_series(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
        .str.strip()
        .str.lower()
    )

def _clean_drug_name_series(s: pd.Series) -> pd.Series:
    return (
        _clean_text_series(s)
        .str.replace(r"\s+\d+\s*(mg|mcg|g|ml)\b", "", regex=True)
        .str.replace(r"\s*(hcl)\b", "", regex=True)
        .str.strip()
    )

def _to_numeric_clean(s: pd.Series) -> pd.Series:
    cleaned = (
        s.astype(str)
        .str.replace(r"[\$,]", "", regex=True)
        .str.strip()
        .str.extract(r"(-?\d+(?:\.\d+)?)", expand=False)
    )
    return pd.to_numeric(cleaned, errors="coerce")


def clean_prescription_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    #TODO: Normalize blank-like values (NA, None, etc) → np.nan

    #########################

    #TODO: clean patient_id

    #TODO: clean fill_date

    #TODO: clean drug_name

    #TODO: clean days_supply

    #TODO: clean quantity_dispensed

    #TODO: clean refill_number

    #TODO: clean patient_age

    #TODO: clean sex

    #TODO: zip_code

    #TODO: prescriber_id

    #TODO: pharmacy_name

    #TODO: copay_amount

    #TODO: adherence_flag

    #TODO: proportion_days_covered (pdc)

    #########################

    #TODO: Drop all duplicate rows

    #TODO: Drop rows if missing critical fields: "patient_id", "fill_date", "drug_name"

    #TODO: Sort by "patient_id", "fill_date"

    df = df.reset_index(drop=True)

    return df