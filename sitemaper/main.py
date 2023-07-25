''' This script crawls a given website and builds a sitemap in XML format. '''
import datetime
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from lxml import etree

# Dictionary representing the HTTP headers to send along with the request.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

# Internal function that attempts to connect to a given URL and extract all hyperlinks present on the page.
def _crawl(session, url, base_url, retries=3, delay=5):
    if not url.startswith(base_url):
        return []

    for _ in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return []

            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.title.string if soup.title else "No Title" # extract page title
            links = [(urljoin(base_url, link.get('href')), title) for link in soup.find_all('a') if link.get('href')]
            return links
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying in {delay} seconds.")
            time.sleep(delay)
    return []

# Internal function that takes a URL, crawls it to find all linked pages, and recursively builds a sitemap by visiting each linked page.
def _build_sitemap(session, url, sitemap, visited, base_url):
    path = url[0].replace(base_url, '')
    if path in visited:
        return

    print(url[0]) # print URL
    sitemap.append(url) # append tuple (url, title)
    visited.add(path)

    links = _crawl(session, url[0], base_url)
    for link in links:
        _build_sitemap(session, link, sitemap, visited, base_url)

# Main function to call to build a sitemap.
def make_sitemap(base_url='https://www.iana.org', filepath='sitemap__iana_org.xml', exclude=None, must_include=None):
    if exclude is None:
        exclude = []
    if must_include is None:
        must_include = []

    print(f"make sitemap for {base_url}\n")

    now = datetime.datetime.now()
    lastmod = now.strftime("%Y-%m-%d")

    sitemap = []
    visited = set()

    # Starts a new HTTP session and initiates the sitemap build process.
    with requests.Session() as session:
        _build_sitemap(session, (base_url, 'Home'), sitemap, visited, base_url)

    # Creates XML format of the sitemap and saves it to a file.
    root = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url, title in sitemap:
        if any(ex in url for ex in exclude) or not all(inc in url for inc in must_include):
            continue
        url_element = etree.SubElement(root, 'url')
        etree.SubElement(url_element, 'loc').text = url
        etree.SubElement(url_element, 'lastmod').text = lastmod
        etree.SubElement(url_element, 'title').text = title

    with open(filepath, 'wb') as file:
        file.write("<?xml version='1.0' encoding='UTF-8'?>\n".encode())
        file.write(etree.tostring(root, pretty_print=True))
    print(f"sitemap for {base_url} with {len(sitemap)} - some are excludet! \n")

# The main part of the script where you specify the site to crawl and where to save the sitemap.
if __name__ == "__main__":
    # filename = 'sitemap__iana_org.xml'
    # base_url = 'https://www.iana.org/help/example-domains'
    filename = 'sitemap__ch_ch.xml'
    base_url = 'https://www.ch.ch'
    exclude = ["@", "#"]
    must_include = ["/", "https://www.ch.ch"]
    make_sitemap(base_url, filename, exclude, must_include)
