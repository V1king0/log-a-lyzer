import re
import numpy as np
import pandas as pd

def detect_anomalies(log_file, pattern, column_name, threshold=3):
    # Read the syslog file into a pandas DataFrame
    with open(log_file, 'r') as file:
        lines = file.readlines()

    # Extract the relevant data using a regular expression pattern
    matches = [re.search(pattern, line) for line in lines]
    data = [match.groupdict() for match in matches if match]

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(data)

    # Convert column values to appropriate data types
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

    # Remove missing or invalid values
    df = df.dropna(subset=[column_name])

    # Extract the column values for anomaly detection
    values = df[column_name].values

    # Calculate the z-scores for the values
    z_scores = (values - np.mean(values)) / np.std(values)

    # Identify the anomalies based on the threshold
    anomalies = np.where(np.abs(z_scores) > threshold)[0]

    # Print the anomalies and their corresponding values
    print("Anomalies:")
    for index in anomalies:
        value = values[index]
        print(f"Value: {value}, Z-Score: {z_scores[index]}")

# Example usage
log_file = "syslog.log"
pattern = r'response_time=(?P<response_time>\d+)'
column_name = "response_time"
detect_anomalies(log_file, pattern, column_name)
