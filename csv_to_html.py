import pandas as pd
from jinja2 import Environment, FileSystemLoader

def csv_to_html(csv_file, template_file, output_html):
    # Read data from CSV
    data = pd.read_csv(csv_file)
    
    # Group data by 'Person' and prepare it for rendering
    # all_persons = {person: group.to_dict('records') for person, group in data.groupby('Person')}

    grouped_data = data.groupby('Person')
    all_persons = {person: group.to_dict('records') for person, group in grouped_data}

    # Sort 'all_persons' by grade, then by the last name extracted from the 'Person' key
    sorted_persons = sorted(all_persons.items(), key=lambda x: (x[1][0]['Grade'], x[0].split(" ")[-1]))

    # Convert the sorted list back to a dictionary
    all_persons_sorted = {person: data for person, data in sorted_persons}

    # Check that each person's grade will render correctly in Jinja2 template (kinda a hack)
    for person in all_persons_sorted:
        if all_persons_sorted[person][0]["Category"] != "Same Gender Same Grade":
            print("Fatal: First item in array is not the same grade, so we'll get incorrect grade")
            return
        
    # print(all_persons["Dylan Lu"][0]["Grade"])

    # Set up Jinja2 environment and render the template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)
    html_out = template.render(all_persons=all_persons_sorted)

    # Write output to an HTML file
    with open(output_html, "w") as file:
        file.write(html_out)


# Example usage
csv_file = "output/all_matches.csv"  # Replace with your CSV file path
template_file = "template/template.html"  # Replace with your HTML template file
output_html = "output/output.html"  # Output HTML file

csv_to_html(csv_file, template_file, output_html)
