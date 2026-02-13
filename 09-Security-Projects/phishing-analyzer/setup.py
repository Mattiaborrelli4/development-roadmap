"""
Setup configuration for Phishing Email Analyzer
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="phishing-analyzer",
    version="1.0.0",
    author="Security Education Project",
    author_email="educational@example.com",
    description="Strumento educativo per l'analisi delle email di phishing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phishing-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: System Administrators",
        "Topic :: Security",
        "Topic :: Education",
        "License :: Other/Proprietary",
        "License :: Free For Educational Use",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "rich>=13.0.0",
        "dnspython>=2.3.0",
        "python-whois>=0.8.0",
        "pyyaml>=6.0",
        "validators>=0.20.0",
        "tldextract>=3.4.0",
        "urlextract>=1.8.0",
        "email-validator>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "phishing-analyzer=main:cli",
        ],
    },
    keywords="phishing security email education defensive",
    project_urls={
        "Documentation": "https://github.com/yourusername/phishing-analyzer/wiki",
        "Source": "https://github.com/yourusername/phishing-analyzer",
        "Bug Reports": "https://github.com/yourusername/phishing-analyzer/issues",
    },
)
