from setuptools import setup, find_packages

setup(
    name='sitemaper',
    version='0.1.7',
    packages=find_packages(),
    url='https://github.com/tabee/sitemaper',
    license='MIT License',
    author='Mario Bee',
    author_email='bee.mario@gmail.com',
    description='A small sitemap generator.',
    install_requires=['bs4', 'lxml', 'requests'],
)
