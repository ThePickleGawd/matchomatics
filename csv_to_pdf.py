import pandas as pd
from jinja2 import Environment, FileSystemLoader


def csv_to_html(csv_file, template_file, output_html):
    # Read data from CSV
    data = pd.read_csv(csv_file)

    # Set up Jinja2 environment
    env = Environment(loader=FileSystemLoader("."))
    template = env.get_template(template_file)

    # Render the template with data
    html_out = template.render(matches=data.to_dict("records"), Name="Sophia")

    # Write output to an HTML file
    with open(output_html, "w") as file:
        file.write(html_out)


# Example usage
csv_file = "output/match_Sophia_Brown.csv"  # Replace with your CSV file path
template_file = "template/template.html"  # Replace with your HTML template file
output_html = "output.html"  # Output HTML file

csv_to_html(csv_file, template_file, output_html)
