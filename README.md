# sitemaper 🕸️🦾

sitemaper is a Python tool for creating sitemaps by crawling a specified website. It generates a sitemap in XML format that includes the URLs and titles of all the pages within the site.

## Installation

To install sitemaper, you need to clone the repository and install it using pip. Run the following commands:

```bash
pip install git+https://github.com/tabee/sitemaper.git
```

## Usage

You can use sitemaper in your Python scripts as follows:

```python
from sitemaper.main import Datasource, make_sitemap

source_01 = Datasource(
    'https://www.bee-gu.ch',
    'sitemap__bee_gu_ch.xml',
    ["#", "mailto:"],
    [".html", "https://www.bee-gu.ch"])

try:
    make_sitemap(source_01.base_url, source_01.filename,
                    source_01.exclude, source_01.must_include)
except Exception as e:
    print("An error occurred:", e)
```

This script will crawl the website at the specified base URL and build a sitemap, which is saved to the specified file. The `exclude` and `must_include` parameters are lists of URL substrings to exclude from or require in the sitemap, respectively.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
