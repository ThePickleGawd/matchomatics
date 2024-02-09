import os
import pandas as pd
import math
import random

# Function to calculate match score as a percent
def calculate_match_score(row1, row2, compare_columns):
    # Points assignment
    dependent_match_points = 5
    exact_match_points = 1.5
    close_match_points = 1.0

    # Initialize score and max possible score
    score = 0.0
    max_score = 0.0

    # Score general questions
    for col in compare_columns:
        max_score += exact_match_points  # Update max score for each question
        if row1[col][0] == row2[col][0]:
            score += exact_match_points  # Exact match
        elif abs(int(row1[col][0]) - int(row2[col][0])) == 1:
            score += close_match_points  # Close match

    # Score dependent questions
    for preference, attribute in dependent_questions:
        max_score += dependent_match_points  # Update max score for each dependent question
        if row1[preference][0] == row2[attribute][0]:
            score += dependent_match_points  # Match between preference and attribute

    # Calculate basic percent match
    percent_match = (score / max_score) if max_score > 0 else 0
    if percent_match < 0.15:
        return round(random.uniform(1.8, 15), 1)

    # Scaled match percent for top matches
    scaled_percent = 0.1 + (percent_match ** 0.5)
    return min(round(scaled_percent * 100, 1), 99.8)


# Dictionary to store matches for each person
matches = {}

# Read the sample data from the CSV
sample_data = pd.read_csv("data.csv")

# Columns to exclude
exclude_columns = ['Name', 'Timestamp', 'Gender', 'Grade', "Username", "ID number", "Email Address"]

# Dependent columns
dependent_questions = [
    ("What do you look for first in others?", "The best thing you have going is"),
    ("You current hair color is", "What hair color do you prefer on others?")
]

# Dynamically create the list of columns to compare
dependent_columns = [col for question in dependent_questions for col in question]
compare_columns = [col for col in sample_data.columns if col not in exclude_columns and col not in dependent_columns]

# Iterate through each person in the data
for index, person in sample_data.iterrows():
    all_matches = []
    
    # Politically incorrect but necessary
    if(person['Gender'] != "Male" and person["Gender"] != "Female"):
        person['Gender'] = "Female"

    # Iterate through all other people for comparison
    for compare_index, compare_person in sample_data.iterrows():
        if person['Name'] != compare_person['Name']:  # Ensure not comparing the same person
            match_score = calculate_match_score(person, compare_person, compare_columns)
            match_info = (
                compare_person['Name'],
                compare_person['Grade'],
                compare_person['Gender'],
                match_score,
            )
            all_matches.append(match_info)

    # Sorting all matches based on score
    sorted_all_matches = sorted(all_matches, key=lambda x: x[3], reverse=True)

    # Selecting top matches based on criteria
    same_gender_same_grade = [m for m in sorted_all_matches if m[2] == person['Gender'] and m[1] == person['Grade']][:10]
    same_gender_diff_grade = [m for m in sorted_all_matches if m[2] == person['Gender'] and m[1] != person['Grade']][:10]
    diff_gender_same_grade = [m for m in sorted_all_matches if m[2] != person['Gender'] and m[1] == person['Grade']][:10]
    diff_gender_diff_grade = [m for m in sorted_all_matches if m[2] != person['Gender'] and m[1] != person['Grade']][:10]
    most_opposite_same_gender = sorted([m for m in all_matches if m[2] == person['Gender']], key=lambda x: x[3])[:5]
    most_opposite_diff_gender = sorted([m for m in all_matches if m[2] != person['Gender']], key=lambda x: x[3])[:5]

    # Store in the matches dictionary
    matches[person['Name']] = {
        "Same Gender Same Grade": same_gender_same_grade,
        "Same Gender Different Grade": same_gender_diff_grade,
        "Different Gender Same Grade": diff_gender_same_grade,
        "Different Gender Different Grade": diff_gender_diff_grade,
        "Most Opposite Same Gender": most_opposite_same_gender,
        "Most Opposite Different Gender": most_opposite_diff_gender,
    }


# Export to CSV
output_dir = "output"
output_files = []

# Initialize an empty DataFrame for all matches
all_matches_df = pd.DataFrame()

# Iterate through each person and their matches in the matches dictionary
for person, person_matches in matches.items():
    # Create DataFrames for each category of matches
    for category, match_list in person_matches.items():
        category_df = pd.DataFrame(match_list, columns=["Name", "Grade", "Gender", "Percent"])
        category_df['Category'] = category
        category_df['Person'] = person  # Add a column indicating to whom these matches belong

        # Append to the main DataFrame
        all_matches_df = pd.concat([all_matches_df, category_df], ignore_index=True)

# Export the combined DataFrame to a single CSV file
output_csv_path = os.path.join(output_dir, 'all_matches.csv')
all_matches_df.to_csv(output_csv_path, index=False)
