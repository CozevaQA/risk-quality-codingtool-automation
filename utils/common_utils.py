# utils/common_utils.py
import base64
from enum import Enum


from datetime import datetime

def is_valid_date(date_str, fmt="%m/%d/%Y"):
    try:
        datetime.strptime(date_str, fmt)
        return True
    except ValueError:
        return False


def decode_base64(data):
    return base64.b64decode(data).decode("utf-8")

def encode_base64(text):
    return base64.b64encode(text.encode()).decode()


# --------------------- HCC Basis File selector -------------------



_MAPPING_FILE_PATHS = {
    "commercial": "testresource/ICD10-Commercial.csv",
    "medicaid": "testresource/ICD10-Medicaid.csv",
    "medicare": "testresource/ICD10-Mapping.csv",
}


def get_mapping_file_path(hcc_type) -> str:
    """
    Returns mapping CSV file path for given HCC type.
    Does NOT load the file.
    """
    try:
        return _MAPPING_FILE_PATHS[hcc_type]
    except KeyError:
        raise ValueError(f"Unsupported HCC type: {hcc_type}")

# - -------------------------------------------------------------------------------------