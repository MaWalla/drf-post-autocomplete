#!/usr/bin/env python
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


INSTALL_REQUIRES = [
    'django',
    'djangorestframework',
    'requests',
]


CLASSIFIERS = [
    'Framework :: Django',
    'Framework :: Django :: 4.0',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.10',
]


PACKAGES = [
    'post_autocomplete',
    'post_autocomplete.migrations',
    'post_autocomplete.models',
    'post_autocomplete.serializer',
    'post_autocomplete.tests',
    'post_autocomplete.tools',
    'post_autocomplete.views',
]


setup(
    name='drf-post-autocomplete',
    version='2023.1.1',
    author='Max Walaschewski',
    author_email='mawalla@protonmail.com',
    description='API implementation for Autocomplete 2.0 from Deutsche Post Direkt',
    license='MIT',
    keywords=['autocomplete', 'post', 'django', 'drf'],
    url='https://github.com/MaWalla/drf-post-autocomplete',
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
    long_description=read('README.md'),
    include_package_data=True,
    zip_safe=False
)
