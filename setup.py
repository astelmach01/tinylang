from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

__version__ = "0.4.2"

setup(
    name="tinylang",
    version=__version__,
    install_requires=requirements,
    packages=find_packages(),
    description="A tiny language interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
