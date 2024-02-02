import pandas as pd
from jinja2 import Environment, FileSystemLoader

def csv_to_html(csv_file, template_file, output_html):
    # Read data from CSV
    data = pd.read_csv(csv_file)

    # Group data by 'Person' and prepare it for rendering
    all_persons = {person: group.to_dict('records') for person, group in data.groupby('Person')}

    # Get the grade
    for person in all_persons:
        if all_persons[person][0]["Category"] != "Same Gender Same Grade":
            print("Fatal: First item in array is not the same grade, so we'll get incorrect grade")
            return

    # Set up Jinja2 environment and render the template
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)
    html_out = template.render(all_persons=all_persons)

    # Write output to an HTML file
    with open(output_html, "w") as file:
        file.write(html_out)


# Example usage
csv_file = "output/all_matches.csv"  # Replace with your CSV file path
template_file = "template/template.html"  # Replace with your HTML template file
output_html = "output/output.html"  # Output HTML file

csv_to_html(csv_file, template_file, output_html)
