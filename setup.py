from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.1.0"

setup(
    name="tinylang",
    version=__version__,
    packages=find_packages(),
    description="A tiny language interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
