import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/compass-visits>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = "compass_visits/VERSION"
print(os.path.join(os.path.dirname(__file__), version_path))
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/compass-visits"
setup(
    name="compass-visits",
    version=VERSION,
    packages=["compass_visits"],
    author="UWIT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        "django~=5.2",
        "django-userservice~=3.2",
        "django-supporttools~=3.6",
        "django-persistent-message~=1.3",
        "uw-restclients-sws~=2.5",
        "uw-restclients-pws~=2.1",
        "uw-restclients-django-utils~=2.3",
        "uw-django-saml2~=1.8",
        "psycopg[c]",
    ],
    license="Apache License, Version 2.0",
    description=(
        "An application for managing advising center checkins for Compass."
    ),
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
