import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="ura",
    version="1.0.0",
    description="unofficial python api wrapper for ura data services api",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/eugenekoh/ura",
    author="Eugene Koh",
    author_email="ekoh016@e.ntu.edu.sg",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ura"],
    include_package_data=True,
    install_requires=["requests"],
)