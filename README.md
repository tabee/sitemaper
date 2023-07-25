#🕸️🦾sitemaper

sitemaper is a Python tool for creating sitemaps by crawling a specified website. It generates a sitemap in XML format that includes the URLs and titles of all the pages within the site.

## Installation

To install sitemaper, you need to clone the repository and install it using pip. Run the following commands:

```bash
git clone https://github.com/tabee/sitemaper.git
cd sitemaper
pip install .
```

## Usage

You can use sitemaper in your Python scripts as follows:

```python
from sitemaper import make_sitemap

filename = 'sitemap__iana_org.xml'
base_url = 'https://www.iana.org/help/example-domains'
exclude = ["#", "@"]
must_include = ["/", "https://www."]

make_sitemap(base_url, filename, exclude, must_include)
```

This script will crawl the website at the specified base URL and build a sitemap, which is saved to the specified file. The `exclude` and `must_include` parameters are lists of URL substrings to exclude from or require in the sitemap, respectively.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
