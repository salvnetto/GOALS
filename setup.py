from setuptools import setup, find_packages

with open("README.md") as f:
    README = f.read()

CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Database",
    "Topic :: Internet"
]

REQUIREMENTS = [
    'pandas',
]

PROJECT_URLS = {
    "Bug Tracker": "https://github.com/salvnetto/GOALS/issues",
    #"Documentation": "https://salvnetto.github.io/goals",
    "Source Code": "https://github.com/salvnetto/GOALS",
}

setup(
    name='GOALS-Football',
    version='1.0.0',
    description= "The GOALS package facilitates game outcome analysis using statistical learning techniques. It is designed for modeling and predicting football match results based on various statistical features.",
    packages= find_packages(),
    long_description= README,
    long_description_content_type= "text/markdown",
    url= "https://github.com/salvnetto/GOALS",
    maintainer= "Salvador Netto",
    maintainer_email= "salvv.netto@gmail.com",
    license= "MIT",
    platforms="any",
    classifiers= CLASSIFIERS,
    install_requires= REQUIREMENTS,
    zip_safe=False,
    python_requires='>3.5',
    project_urls=PROJECT_URLS,
)