# Markdown to PDF Converter

This Python script converts Markdown files to PDF format. It supports multiple file processing, table of contents generation, syntax highlighting, and more.

## Features

- Convert single or multiple Markdown files to PDF
- Optional table of contents generation
- Syntax highlighting for code blocks
- Image handling
- Progress bar for multiple file processing
- Error handling and logging
- Command-line interface with help function
- Custom CSS styling support
- Page numbering option

## Requirements

- Python 3.6+
- wkhtmltopdf (external dependency)

## Installation

1. Clone this repository or download the script.

2. Install the required Python packages:

   ```
   pip install -r requirements.txt
   ```

3. The `requirements.txt` file is included in the repository and contains all necessary Python dependencies.

## Repository Contents

- `mdtopdf.py`: The main Python script for converting Markdown to PDF.
- `requirements.txt`: A file listing all required Python packages.
- `README.md`: This file, containing usage instructions and project information.

## Usage

Run the script from the command line with various options:

```
python mdtopdf.py [OPTIONS] INPUT_FILE [INPUT_FILE ...]
```

### Available Flags

- `-o, --output`: Specify the output PDF file name (default: input filename with .pdf extension)
- `-t, --toc`: Generate a table of contents (default: False)
- `-c, --css`: Specify a custom CSS file for styling (default: None)
- `-p, --page-numbers`: Add page numbers to the PDF (default: False)
- `-v, --verbose`: Enable verbose output for debugging (default: False)
- `-h, --help`: Show the help message and exit

### Examples

1. Convert a single file:
   ```
   python mdtopdf.py input.md
   ```

2. Convert multiple files with a table of contents:
   ```
   python mdtopdf.py -t file1.md file2.md file3.md
   ```

3. Use custom CSS and add page numbers:
   ```
   python mdtopdf.py -c custom_style.css -p input.md
   ```

4. Specify output filename and enable verbose mode:
   ```
   python mdtopdf.py -o output.pdf -v input.md
   ```

For more information on usage and options, run:
```
python mdtopdf.py --help
```