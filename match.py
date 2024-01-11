import os
import pandas as pd


# Function to calculate match score as a percent
def calculate_match_score(row1, row2, max_diff):
    compare_columns = [
        "Favorite season?",
        "Favorite day of week?",
        "What do you look for first in others?",
        "Life would stink without",
        "When someone says get lost you:",
    ]
    total_difference = sum(
        abs(int(row1[col].split(" - ")[0]) - int(row2[col].split(" - ")[0]))
        for col in compare_columns
    )
    # Calculate percent match (higher score means more similarity)
    match_score = ((max_diff - total_difference) / max_diff) * 100
    return round(match_score, 2)


# Maximum possible difference (for calculating percent match)
max_diff = (
    len(
        [
            "Favorite season?",
            "Favorite day of week?",
            "What do you look for first in others?",
            "Life would stink without",
            "When someone says get lost you:",
        ]
    )
    * 3
)  # Each question has max diff of 3

# Dictionary to store matches for each person
matches = {}

# Read the sample data from the CSV
sample_data = pd.read_csv("data.csv")

# Iterate through each person in the data
for index, person in sample_data.iterrows():
    same_grade_matches = []
    different_grade_matches = []

    # Iterate through all other people for comparison
    for compare_index, compare_person in sample_data.iterrows():
        if person["Gender"] != compare_person["Gender"]:
            match_score = calculate_match_score(person, compare_person, max_diff)

            # Check for same grade
            if (
                person["What grade are you in?"]
                == compare_person["What grade are you in?"]
            ):
                same_grade_matches.append(
                    (
                        compare_person["Name"],
                        compare_person["What grade are you in?"],
                        match_score,
                    )
                )
            else:
                different_grade_matches.append(
                    (
                        compare_person["Name"],
                        compare_person["What grade are you in?"],
                        match_score,
                    )
                )

    # Sort and get top matches
    sorted_same_grade_matches = sorted(
        same_grade_matches, key=lambda x: x[2], reverse=True
    )[:15]
    sorted_different_grade_matches = sorted(
        different_grade_matches, key=lambda x: x[2], reverse=True
    )[:10]

    # Store in the matches dictionary
    matches[person["Name"]] = {
        "Same Grade": sorted_same_grade_matches,
        "Different Grade": sorted_different_grade_matches,
    }

# Export to CSV
output_dir = "output"
output_files = []

for person, person_matches in matches.items():
    # Combine both categories of matches into a single DataFrame
    same_grade_df = pd.DataFrame(
        person_matches["Same Grade"], columns=["Name", "Grade", "Percent"]
    )
    different_grade_df = pd.DataFrame(
        person_matches["Different Grade"],
        columns=["Name", "Grade", "Percent"],
    )
    combined_df = pd.concat(
        [
            same_grade_df.assign(Category="Same Grade"),
            different_grade_df.assign(Category="Different Grade"),
        ]
    )

    # Save to CSV in the output directory
    match_csv_path = os.path.join(output_dir, f'match_{person.replace(" ", "_")}.csv')
    combined_df.to_csv(match_csv_path, index=False)
    output_files.append(match_csv_path)
