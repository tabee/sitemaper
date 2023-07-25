# sitemaper

## install

```bash
pip install git+https://github.com/tabee/sitemaper.git
```

## use it

this will generate a file with the name sitemap_iana_org.xml

```python
from my_sitemap_generator.main import make_sitemap
NAME = '_iana_org'
URL = 'https://www.iana.org/help/example-domains'
make_sitemap(URL, NAME)
```
