import os
import pandas as pd

# Function to calculate match score as a percent
def calculate_match_score(row1, row2, compare_columns):
    # Points assignment
    exact_match_points = 10
    close_match_points = 5

    # Initialize score and max possible score
    score = 0
    max_score = 0

    # Score general questions
    for col in compare_columns:
        max_score += exact_match_points  # Update max score for each question
        if row1[col][0] == row2[col][0]:
            score += exact_match_points  # Exact match
        elif abs(int(row1[col][0]) - int(row2[col][0])) == 1:
            score += close_match_points  # Close match

    # Score dependent questions
    for preference, attribute in dependent_questions:
        max_score += exact_match_points  # Update max score for each dependent question
        if row1[preference] == row2[attribute]:
            score += exact_match_points  # Match between preference and attribute

    # Calculate percent match
    percent_match = (score / max_score) * 100 if max_score > 0 else 0
    return percent_match


# Dictionary to store matches for each person
matches = {}

# Read the sample data from the CSV
sample_data = pd.read_csv("data.csv")

# Columns to exclude
exclude_columns = ['Name', 'Timestamp', 'Gender', 'Grade', "Username"]

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

    # Iterate through all other people for comparison
    for compare_index, compare_person in sample_data.iterrows():
        if person['Name'] != compare_person['Name']:  # Assuming an 'ID' column
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
    most_opposite_matches = sorted(all_matches, key=lambda x: x[3])[:3]  # Lowest scores
    same_gender_matches = [m for m in sorted_all_matches if m[2] == person['Gender']][:5]
    same_grade_matches = [m for m in sorted_all_matches if m[1] == person['Grade']][:10]
    different_grade_matches = [m for m in sorted_all_matches if m[1] != person['Grade']][:5]

    # Store in the matches dictionary
    matches[person['Name']] = {
        "Most Opposite": most_opposite_matches,
        "Same Gender": same_gender_matches,
        "Same Grade": same_grade_matches,
        "Different Grade": different_grade_matches,
    }

# Export to CSV
output_dir = "output"
output_files = []

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over the matches dictionary to create and save CSV files
for person, person_matches in matches.items():
    # Create DataFrames for each category of matches
    same_grade_df = pd.DataFrame(
        person_matches["Same Grade"], columns=["Name", "Grade", "Gender", "Percent"]
    ).assign(Category="Same Grade")

    different_grade_df = pd.DataFrame(
        person_matches["Different Grade"], columns=["Name", "Grade", "Gender", "Percent"]
    ).assign(Category="Different Grade")

    same_gender_df = pd.DataFrame(
        person_matches["Same Gender"], columns=["Name", "Grade", "Gender", "Percent"]
    ).assign(Category="Same Gender")

    most_opposite_df = pd.DataFrame(
        person_matches["Most Opposite"], columns=["Name", "Grade", "Gender", "Percent"]
    ).assign(Category="Most Opposite")

    # Combine all categories into a single DataFrame
    combined_df = pd.concat(
        [same_grade_df, different_grade_df, same_gender_df, most_opposite_df]
    )

    # Save to CSV in the output directory
    match_csv_path = os.path.join(output_dir, f'match_{person.replace(" ", "_")}.csv')
    combined_df.to_csv(match_csv_path, index=False)
    output_files.append(match_csv_path)
