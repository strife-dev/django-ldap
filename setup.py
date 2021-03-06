from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, "readme.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="django-ldap",
    description="Django LDAP3.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Strife-Dev",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    url="https://github.com/strife-dev/django-ldap",
    license="BSD-3-Clause",
    license_file="LICENSE",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration :: Authentication/Directory :: LDAP",
    ],
    project_urls={
        "Documentation": "https://github.com/strife-dev/django-ldap/blob/master/documentation/readme.md",
        "Source": "https://github.com/strife-dev/django-ldap",
        "Tracker": "https://github.com/strife-dev/django-ldap/issues",
    },
    packages=find_packages(),
    install_requires=[
        "django>=2.2",
        "ldap3>=2.7",
        "pytest>=3.9",
    ],
    python_requires=">=3.7",
)
