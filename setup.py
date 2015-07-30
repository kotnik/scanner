import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md")) as f:
    README = f.read()

setup(
    name="scanner",
    version="1.0",
    description="Test sites for SSL vulnerabilities",
    long_description=README,
    keywords="ssl security",
    author="Nikola Kotur",
    author_email="kotnick@gmail.com",
    packages=find_packages(),
    package_data = {
        "zooned": [ "VERSION" ],
    },
    scripts=[ "bin/scanner" ],
    install_requires=[
        "gevent",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2 :: Only",
    ],
)
