from setuptools import setup, find_packages

from conf_loader import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="conf_loader",
    packages=find_packages(),
    version=__version__,
    url="https://github.com/sfahad1414/configloader",
    license="MIT",
    author="Fahad Ali Shaikh",
    author_email="shaikhfahad2526@gmail.com",
    description="Simple configuration file loader",
    install_requires=["pyyaml", "toml", "loguru"],
    python_requires=">=3.5",
    include_package_data=True,
    platforms="any",
    test_suite="tests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)