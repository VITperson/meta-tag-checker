# Meta Tag Checker

A Python script to extract meta titles and descriptions from multiple web pages.

## Features

- Extracts `<title>` tags and `<meta name="description">` content from web pages
- Processes multiple URLs from a CSV file
- Outputs results to a CSV file with URL, status, title, and description
- Configurable delay between requests to be respectful to servers
- Easy configuration through external config file

## Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd meta-tag-checker
```

2. Copy the example configuration file:
```bash
cp config.py.example config.py
```

3. Edit `config.py` with your settings:
```python
BASE_URL = "https://www.yourwebsite.com"
INPUT_FILE = "pages.csv"
OUTPUT_FILE = "meta_check_results.csv"
DELAY_SECONDS = 0.5
REQUEST_TIMEOUT = 10
```

## Usage

1. Create an input CSV file with URL paths (one per line):
```
/en/about-us
/en/contact
/en/products
```

2. Run the script:
```bash
python3 check_meta.py
```

3. Check the output CSV file for results with columns:
   - **URL**: Full URL that was checked
   - **Status**: Found/Not Found/Error
   - **Meta Title**: Content of the `<title>` tag
   - **Meta Description Content**: Content of the meta description tag

## Configuration Options

Edit `config.py` to customize:

- `BASE_URL`: Base domain to prepend to paths (without trailing slash)
- `INPUT_FILE`: CSV file containing URL paths to check
- `OUTPUT_FILE`: Where to save the results
- `DELAY_SECONDS`: Delay between requests (default: 0.5)
- `REQUEST_TIMEOUT`: Timeout for each request in seconds (default: 10)

## Example

Input file (`pages.csv`):
```
/en/home
/en/about
/en/contact
```

Output file (`meta_check_results.csv`):
```csv
URL,Status,Meta Title,Meta Description Content
https://www.example.com/en/home,Found,Home - Example Company,Welcome to our homepage
https://www.example.com/en/about,Found,About Us - Example Company,Learn more about our company
https://www.example.com/en/contact,Found,Contact - Example Company,Get in touch with us
```

## License

MIT License - feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
