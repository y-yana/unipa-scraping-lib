from setuptools import setup, find_packages

setup(
    name="test_code",
    version='1.3',
    description='test',
    author='y-yana',
    url='https://github.com/y-yana/unipa-scraping-lib',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      test_code = test_code.test_code:call
      cli_test = test_code.cli_test:execute
    """,
    install_requires=open('requirements.txt').read().splitlines(),
)
