from setuptools import setup, find_packages

setup(
    name="scraping",
    version='1.6',
    description='test',
    author='y-yana',
    url='https://github.com/y-yana/unipa-scraping-lib',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      scraping = scraping.scraping:main
      test_code = scraping.test_code:call
      cli_test = scraping.cli_test:execute
    """,
    install_requires=open('requirements.txt').read().splitlines(),
)
