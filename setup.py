#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fp:
    setuptools.setup(
        name="googlesheets",
        version="0.0.1",
        author="misha n. sawangwan",
        author_email="misha.sawangwan@gmail.com",
        description="googlesheets client",
        long_description=fp.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/msawangwan/googlesheets",
        packages=setuptools.find_packages(include=['googlesheets']),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        install_requires=[
            'google-api-python-client',
            'google-auth-httplib2',
            'google-auth-oauthlib',
            'oauth2client',
        ],
        python_requires='>=3.8',
    )
