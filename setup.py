from setuptools import setup, find_packages

setup(
    name='sitemaper',
    version='0.1.0',
    packages=find_packages(),
    url='https://github.com/tabee/sitemaper',
    license='Apache License',
    author='Mario Bee',
    author_email='bee.mario@gmail.com',
    description='A small sitemap generator.',
    install_requires=['etree', 'beautifulsoup4'],
)