import os
import yaml
import zipfile
import urllib.request
import shutil
from datetime import date

# CONFIG

DATA_DIR = "data"
DATA_URL = "https://cricsheet.org/downloads/t20s.zip"
ZIP_PATH = "t20s.zip"
EXTRACT_DIR = "t20s_tmp"

# DATA BOOTSTRAP


def ensure_data_present():
    """
    Ensure T20 YAML data exists locally.
    Downloads and extracts it if missing.
    """
    if os.path.exists(DATA_DIR) and any(
        f.endswith(".yaml") or f.endswith(".yml") for f in os.listdir(DATA_DIR)
    ):
        print("Data already present.")
        return

    print("Data not found. Downloading T20 dataset.")

    os.makedirs(DATA_DIR, exist_ok=True)

    # Download ZIP
    urllib.request.urlretrieve(DATA_URL, ZIP_PATH)

    # Extract ZIP
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    # Move YAML files into data/
    for root, _, files in os.walk(EXTRACT_DIR):
        for file in files:
            if file.endswith(".yaml") or file.endswith(".yml"):
                src = os.path.join(root, file)
                dst = os.path.join(DATA_DIR, file)
                shutil.move(src, dst)

    # Cleanup
    os.remove(ZIP_PATH)
    shutil.rmtree(EXTRACT_DIR)

    print("Data download and extraction complete.")

# UTILITIES

def normalise_date(d):
    """
    Convert YAML dates to ISO string format.
    """
    if isinstance(d, date):
        return d.isoformat()
    return str(d)

def list_yaml_files(directory):
    """
    Return YAML files sorted by numeric match ID.
    """
    files = [
        f for f in os.listdir(directory)
        if f.endswith(".yaml") or f.endswith(".yml")
    ]

    # Sort chronologically by match ID
    return sorted(files, key=lambda x: int(x.split(".")[0]))

# YAML PARSING

def parse_yaml(file_path):
    """
    Load and normalise a single match YAML.
    """
    with open(file_path, "r") as file:
        content = yaml.safe_load(file)

    # Normalise match dates
    if "info" in content and "dates" in content["info"]:
        content["info"]["dates"] = [
            normalise_date(d) for d in content["info"]["dates"]
        ]

    return content

def load_matches(directory=DATA_DIR):
    """
    Generator that yields (match_id, match_dict)
    one match at a time, in chronological order.
    """
    for filename in list_yaml_files(directory):
        file_path = os.path.join(directory, filename)
        match_id = filename.split(".")[0]
        yield match_id, parse_yaml(file_path)

# MAIN

if __name__ == "__main__":
    ensure_data_present()

    # Print first few matches to verify ordering + dates
    for i, (match_id, match) in enumerate(load_matches()):
        print(match_id, match["info"]["dates"])
        if i == 4:
            break
