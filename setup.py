"""
PYPI-REL
"""

import os
from setuptools import setup, find_packages

import __about__

setup(
    name=__about__.__title__,
    version=__about__.__version__,
    license=__about__.__license__,
    author=__about__.__author__,
    author_email=__about__.__email__,
    description=__about__.__summary__,
    url=__about__.__uri__,
    long_description="",
    py_modules=['pypi_up'],
    entry_points=dict(console_scripts=[
        'pypi-up=pypi_up:main'
    ]),
    include_package_data=True,
    packages=find_packages(),
    install_requires=["reversionup==0.4.0",
                      "sh==1.11"],
    keywords=["reversionup"],
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    zip_safe=False
)

