from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

setup(
    name="conveyance",
    version="0.0.1",
    author="Scott McCormack",
    author_email="scott.mccormack@quenda.io",
    description="Python library for conveyor design",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ScottMcCormack/conveyance",
    project_urls={
        "Bug Tracker": "https://github.com/ScottMcCormack/conveyance/issues",
        'Source': 'https://github.com/ScottMcCormack/conveyance',
    },
    classifiers=[
        "Development Status :: 1 - Planning",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",

    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
