# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, December 28th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import setuptools

with open("Readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

try:
    # if have requirements.txt file inside the folder
    with open("requirements.txt", "r", encoding="utf-8") as f:
        modules_needed = [i.strip() for i in f.readlines()]
except Exception:
    modules_needed = []

setuptools.setup(
    name="utdf2gmns",  # Replace with your own username
    version="0.2.6",
    author="Xiangyong Luo, Dr.Xuesong (Simon) Zhou",
    author_email="luoxiangyong01@gmail.com",
    description="This open-source package is a tool to convert utdf file to GMNS format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/asu-trans-ai-lab/utdf2gmns",

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=modules_needed,

    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'': ['*.txt', '*.xls', '*.xlsx', '*.csv'],
                  "test_data": ['*.xls']},
    project_urls={
        'Homepage': 'https://github.com/xyluo25/utdf2gmns',
        'Documentation': 'https://utdf2gmns.readthedocs.io/en/latest/',
        # 'Bug Tracker': '',
        # 'Source Code': '',
        # 'Download': '',
        # 'Publication': '',
        # 'Citation': '',
        # 'License': '',
        # 'Acknowledgement': '',
        # 'FAQs': '',
        # 'Contact': '',
    }
)