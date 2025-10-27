import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/app_name>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = "app_name/VERSION"
print(os.path.join(os.path.dirname(__file__), version_path))
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/app_name"
setup(
    name="app_name",
    version=VERSION,
    packages=["app_name"],
    author="UW-IT",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        "django~=5.2",
    ],
    license="Apache License, Version 2.0",
    description="",
    long_description=README,
    url=url,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
)
