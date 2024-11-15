#!/usr/bin/python3

# CHALLENGE: Scrape Scotland 'Ballot Box' Local Election Data

# CODE REVISION: Ejimofor Nwoye, Campaign Lab, Newspeak House, London, England, 11th November 2024

import requests
import pdfplumber
import re
import json

# URL of the PDF file
url = "https://www.midlothian.gov.uk/downloads/file/4582/ward_3_dalkeith_preferences_by_ballot_box_report"

# Download the PDF
response = requests.get(url)
pdf_path = "/mnt/data/dalkeith_preferences_report.pdf"

with open(pdf_path, "wb") as f:
    f.write(response.content)

# Initialize an empty list to hold ballot box data
ballot_data = []

# Function to parse and extract ballot box data
def parse_ballot_data(text):
    ballot_boxes = []
    # Define regex patterns to capture relevant information
    pattern = re.compile(r"Ballot Box (\d+).*?Candidate.*?\n((?:.*?\n)+?)Total")
    matches = pattern.findall(text)

    # Process each ballot box match
    for match in matches:
        ballot_box_id = match[0]
        candidate_data = match[1].strip().split("\n")

        # Store candidates and their vote counts
        candidates = []
        for line in candidate_data:
            # Example pattern for "Candidate Name: Vote Count"
            candidate_match = re.match(r"(.*?):\s*(\d+)", line)
            if candidate_match:
                candidate_name = candidate_match.group(1).strip()
                votes = int(candidate_match.group(2).strip())
                candidates.append({"name": candidate_name, "votes": votes})

        ballot_boxes.append({"ballot_box_id": ballot_box_id, "candidates": candidates})

    return ballot_boxes

# Extract text from PDF and parse
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        ballot_data.extend(parse_ballot_data(text))

# Write data to JSON file
output_path = "/mnt/data/ballot_data.json"
with open(output_path, "w") as f:
    json.dump(ballot_data, f, indent=4)

print(f"Ballot box data extracted and saved to {output_path}")


