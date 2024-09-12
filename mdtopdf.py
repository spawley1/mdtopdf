import pdfkit
import sys
import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import logging
from pygments.formatters import HtmlFormatter
from markdown.extensions.codehilite import CodeHiliteExtension
import subprocess

try:
    import markdown
    import pdfkit
    from bs4 import BeautifulSoup
    from tqdm import tqdm
    from pygments.formatters import HtmlFormatter
except ImportError as e:
    print(f"Error: Missing required dependency. {str(e)}")
    print("Please install all required packages using: pip install markdown pdfkit beautifulsoup4 tqdm pygments")
    sys.exit(1)

def generate_toc(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    toc = ["<h2>Table of Contents</h2>", "<ul>"]
    for header in soup.find_all(['h1', 'h2', 'h3']):
        toc.append(f'<li><a href="#{header.get("id")}">{header.text}</a></li>')
    toc.append("</ul>")
    return '\n'.join(toc)

def markdown_to_pdf(input_file, include_toc=False):
    try:
        # Get the directory and filename of the input file
        input_dir = os.path.dirname(input_file)
        input_filename = os.path.basename(input_file)

        # Create the output filename (replace .md with .pdf)
        output_filename = os.path.splitext(input_filename)[0] + '.pdf'
        output_file = os.path.join(input_dir, output_filename)

        # Read the Markdown file
        with open(input_file, 'r', encoding='utf-8') as file:
            markdown_text = file.read()

        # Setup extensions
        extensions = [
            'markdown.extensions.extra',
            CodeHiliteExtension(pygments_style='default', noclasses=True),
            'markdown.extensions.toc'
        ]

        # Convert Markdown to HTML
        html = markdown.markdown(markdown_text, extensions=extensions)

        # Generate table of contents if requested
        toc = generate_toc(html) if include_toc else ""

        # Get the CSS for syntax highlighting
        highlight_css = HtmlFormatter().get_style_defs('.codehilite')

        # Add styling and optional TOC to the HTML
        styled_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; padding: 20px; }}
                h1, h2, h3 {{ color: #333; }}
                code {{ background-color: #f4f4f4; padding: 2px 5px; }}
                {highlight_css}
            </style>
        </head>
        <body>
        {toc}
        {html}
        </body>
        </html>
        """

        # Convert HTML to PDF
        pdfkit.from_string(styled_html, output_file)
        logging.info(f"PDF created: {output_file}")
        return True
    except Exception as e:
        logging.error(f"Error processing {input_file}: {str(e)}")
        return False

def process_files(files, include_toc):
    successful = 0
    failed = 0
    for file in tqdm(files, desc="Processing files"):
        if markdown_to_pdf(file, include_toc):
            successful += 1
        else:
            failed += 1
    return successful, failed

def check_wkhtmltopdf():
    try:
        subprocess.run(['wkhtmltopdf', '-v'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("Error: wkhtmltopdf is not installed or not in PATH.")
        print("Please install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Convert Markdown files to PDF")
    parser.add_argument('input', nargs='+', help="Input Markdown file(s)")
    parser.add_argument('-t', '--toc', action='store_true', help="Include table of contents")
    parser.add_argument('-v', '--verbose', action='store_true', help="Increase output verbosity")
    args = parser.parse_args()

    # Add this check
    if not args.input:
        parser.error("At least one input file is required.")

    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

    check_wkhtmltopdf()
    successful, failed = process_files(args.input, args.toc)
    print(f"Conversion complete. Successful: {successful}, Failed: {failed}")

if __name__ == "__main__":
    main()
