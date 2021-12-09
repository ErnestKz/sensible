"""Python setup.py for sensible package"""
import io
import os
from setuptools import find_packages, setup


def read(*paths, **kwargs):
    """Read the contents of a text file safely.
    >>> read("sensible", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """

    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


def read_requirements(path):
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(('"', "#", "-", "git+"))
    ]


setup(
    name="sensible",
    version=read("sensible", "VERSION"),
    description="Awesome sensible created by ErnestKz",
    url="https://github.com/ErnestKz/sensible/",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="ErnestKz",
    install_requires=read_requirements("requirements.txt"),
    entry_points={
        "console_scripts": ["sensible = sensible.__main__:main"]
    },
)
