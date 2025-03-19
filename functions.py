import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from natsort import natsorted
import re

from config import *


def get_sorted_text_files(directory):
    try:
      
        files = os.listdir(directory)
        text_files = [file for file in files if file.endswith('.txt')]
        sorted_text_files = natsorted(text_files)
        
        return sorted_text_files
    except FileNotFoundError:
        print(f"Error: The directory '{directory}' does not exist.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
def append_suffix(array, suffix):
    for row in array:
        if len(row) > 0:  # Ensure the row is not empty
            row[0] = str(row[0]) + suffix
    return array

def extract_measurement_data(file_path, measurement_name):
    # ChatGPT parsing special 
    """
    Extracts the data for a given measurement from an LTspice output file.

    Parameters:
        file_path (str): The path to the file.
        measurement_name (str): The name of the measurement to extract.
            For example, "overshoot", "i_max", etc.

    Returns:
        pd.DataFrame: A DataFrame containing the measurement data.
    
    Raises:
        ValueError: If the measurement name is not found or no data is extracted.
    """
    def split_line(line):
        # If tabs are used, split on them; otherwise fall back on whitespace.
        if "\t" in line:
            return [token.strip() for token in line.split("\t") if token.strip() != ""]
        else:
            return [token.strip() for token in line.split() if token.strip() != ""]
    
    capturing = False  # Are we in the block for our measurement?
    columns = None     # The header (column names) of the block
    data_rows = []     # The list of data rows

    with open(file_path, "r") as f:
        for line in f:
            stripped = line.strip()
            # Look for a measurement header
            if stripped.startswith("Measurement:"):
                # If we were already capturing data, then a new measurement block has started.
                if capturing:
                    break
                # Otherwise, check if this is the measurement we want
                parts = stripped.split(":", 1)
                if len(parts) > 1 and parts[1].strip() == measurement_name:
                    capturing = True
                    continue  # move on to the next line
            if capturing:
                # If we haven't gotten the header row yet, then skip blank lines until we get it.
                if columns is None:
                    if stripped == "":
                        continue
                    columns = split_line(line)
                    continue
                else:
                    # End the data block if we hit a blank line or a new measurement header
                    if stripped == "" or stripped.startswith("Measurement:"):
                        break
                    tokens = split_line(line)
                    # We expect the first column to be a step number. (You might want to adjust this if needed.)
                    if tokens and tokens[0].isdigit():
                        data_rows.append(tokens)
                    else:
                        # If the row doesn’t start with a digit, assume the block has ended.
                        break

    if not data_rows:
        raise ValueError(f"Measurement '{measurement_name}' not found or no data extracted.")
    
    # Build the DataFrame
    df = pd.DataFrame(data_rows, columns=columns)
    # Attempt to convert all columns to numeric types when possible.
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='ignore')
    return df


def delete_integer_named_files(directory):
    """
    Deletes all files in the given directory whose names are only integers and have no file extension.
    
    Parameters:
        directory (str): Path to the directory to scan.
    """
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a valid directory.")
        return

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Check if it's a file and if the filename consists only of digits
        if os.path.isfile(file_path) and re.fullmatch(r"\d+", filename):
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")

def clearDPTFiles():
    """
    Just an abstraction of the delete_integer_named_files for the DPT directory.
    """
    print("Deleting existing DPT files...")
    delete_integer_named_files(DPT_OUT_DIR)
    print("Deleted existing DPT files")
    return 1


import os
import shutil

def copy_files(source_dir, destination_dir):
    """
    Copies all files from source_dir to destination_dir.
    
    Parameters:
        source_dir (str): Path to the source directory.
        destination_dir (str): Path to the destination directory.
    """
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    
    # Ensure destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    # Loop through all files in the source directory
    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        destination_file = os.path.join(destination_dir, filename)

        # Check if it's a file (not a subdirectory)
        if os.path.isfile(source_file):
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {source_file} → {destination_file}")