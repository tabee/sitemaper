''' This script crawls a given website and builds a sitemap in XML format. '''
import datetime
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from lxml import etree


class Datasource:
    def __init__(self, base_url, filename, exclude, must_include):
        self.base_url = base_url
        self.filename = filename
        self.exclude = exclude
        self.must_include = must_include


# Dictionary representing the HTTP headers to send along with the request.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3'
}

# Internal function that attempts to connect to a given URL and extract all hyperlinks present on the page.


def _crawl(session, url, base_url, retries=5, delay=15):
    if not url.startswith(base_url):
        return []

    for _ in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=15)
            if response.status_code != 200:
                return []

            # Falls die Response eine HTML-Seite ist
            if 'text/html' in response.headers['Content-Type']:
                soup = BeautifulSoup(response.content, 'html.parser')
                title = soup.title.string if soup.title else "No Title"  # extract page title
                links = [(urljoin(base_url, link.get('href')), title)
                         for link in soup.find_all('a') if link.get('href')]
                return links

            # Falls die Response eine PDF ist
            elif 'application/pdf' in response.headers['Content-Type']:
                return [(url, "PDF-Datei")]

            else:
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}. Retrying in {delay} seconds.")
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred while processing {url}: {e}")
            return []
    return []


# Internal function that takes a URL, crawls it to find all linked pages, and recursively builds a sitemap by visiting each linked page.


def _build_sitemap(session, url, sitemap, visited, base_url, exclude):
    path = url[0].replace(base_url, '')
    if path in visited:
        return
    for ex in exclude:  # kommt eines der exclude in der url vor, dann return, gefährlich, da auch teilstrings
        if ex in path:
            return

    print(url[0])  # print URL
    sitemap.append(url)  # append tuple (url, title)
    visited.add(path)

    links = _crawl(session, url[0], base_url)
    for link in links:
        _build_sitemap(session, link, sitemap, visited, base_url, exclude)

# Main function to call to build a sitemap.


def make_sitemap(base_url='https://www.iana.org', filepath='sitemap__iana_org.xml', exclude=['#'], must_include=['.org']):
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
        _build_sitemap(session, (base_url, 'Home'),
                       sitemap, visited, base_url, exclude)

    # Creates XML format of the sitemap and saves it to a file.
    root = etree.Element(
        'urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for url, title in sitemap:
        if any(ex in url for ex in exclude) or not all(inc in url for inc in must_include):
            continue
        url_element = etree.SubElement(root, 'url')
        etree.SubElement(url_element, 'loc').text = url
        etree.SubElement(url_element, 'lastmod').text = lastmod
        etree.SubElement(url_element, 'title').text = title

    with open(filepath, 'wb') as file:
        file.write("<?xml version='1.0' encoding='UTF-8'?>\n".encode('utf-8'))
        #file.write(etree.tostring(root, pretty_print=True))
        file.write(etree.tostring(root, pretty_print=True, encoding='UTF-8')).encode('utf-8')
    print(
        f"sitemap for {base_url} with {len(sitemap)} - some are excludet! \n")


# The main part of the script where you specify the site to crawl and where to save the sitemap.
if __name__ == "__main__":

    source_00_br = Datasource('https://admin.ch',
                              'sitemap__admin_ch.xml',
                              ['/fr/', '/it/',  '/en/', '/rm/', '#', 'mailto:', '.zip', 'mp3', 'mp4'],
                              ['https://admin.ch', '/de/'])
    source_01_eak = Datasource('https://www.eak.admin.ch',
                               'sitemap__eak_admin_ch.xml',
                               ['/fr/', '/it/', '/en/'],
                               ['https://www.eak.admin.ch', '/de/', '/'])
    source_02_zas = Datasource('https://www.zas.admin.ch',
                               'sitemap__zas_admin_ch.xml',
                               ['/fr/', '/it/',  '/en/', 'es/', '#', 'mailto:'],
                               ['/de/', 'https://www.zas.admin.ch'])
    source_03_bee = Datasource('https://www.bee-gu.ch',
                               'sitemap__bee_gu_ch.xml',
                               ['/fr/', '/it/',  '/en/', 'es/', '#', 'mailto:'],
                               ['https://www.bee-gu.ch', '/', '.html'])

    source = source_03_bee

    try:
        make_sitemap(source.base_url, source.filename,
                     source.exclude, source.must_include)
    except Exception as e:
        print("An error occurred:", e)
