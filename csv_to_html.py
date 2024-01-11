import pandas as pd
from jinja2 import Environment, FileSystemLoader

# TODO
# Create file and add html headers
# Open all csv, run render and insert
# Add closing html

def csv_to_html(csv_file, template_file, output_html):
    # Read data from CSV
    data = pd.read_csv(csv_file)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)

    # Render the template with data
    html_out = template.render(matches=data.to_dict("records"), Name="Alex")

    # Write output to an HTML file
    with open(output_html, "w") as file:
        file.write(html_out)


# Example usage
csv_file = "output/match_Alex_Davis.csv"  # Replace with your CSV file path
template_file = "template/template.html"  # Replace with your HTML template file
output_html = "output.html"  # Output HTML file

csv_to_html(csv_file, template_file, output_html)
