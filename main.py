import argparse
import datetime
import pandas

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_type(number: int) -> str:

    number = abs(number) % 100
    num_last = number % 10

    if 11 <= number <= 19:
        return "лет"
    if num_last == 1:
        return "год"
    if 2 <= num_last <= 4:
        return "года"

    return "лет"


def get_wine_catalog(file_path: str, sheet_name: str = 'Лист1') -> dict:

    df = pandas.read_excel(file_path,
                           sheet_name=sheet_name,
                           keep_default_na=False)

    catalog = {
        category: group.drop(columns='Категория').to_dict(orient='records')
        for category, group in df.groupby('Категория')
    }

    return catalog


def render_page(file_path: str) -> None:

    env = Environment(loader=FileSystemLoader('.'),
                      autoescape=select_autoescape(['html', 'xml']))

    template = env.get_template('template.html')

    launch_year = 1920
    current_year = datetime.datetime.now().year
    age = current_year - launch_year
    year_type = get_year_type(age)

    wines = get_wine_catalog(file_path)

    rendered_page = template.render(
        age=age,
        year_type=year_type,
        wines=wines,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():

    parser = argparse.ArgumentParser(description="Wine webpage")
    parser.add_argument(
        "--file",
        default="wine.xlsx",
        help="Path to the Excel file with wine data (default: wine3.xlsx)",
    )
    args = parser.parse_args()

    render_page(args.file)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
