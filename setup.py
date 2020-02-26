#!/usr/bin/env python
"""
Install wagtailmodelchooser using setuptools
"""
from setuptools import find_packages, setup

with open('wagtailbirdsong/version.py', 'r') as f:
    version = None
    exec(f.read())

with open('README.md', 'r') as f:
    readme = f.read()

setup(
    name='wagtailbirdsong',
    version=version,
    description='Create and send email campaigns from Wagtail',
    long_description=readme,
    author='Jonny Scholes',
    author_email='jonny@neonjungle.studio',

    install_requires=['wagtail>=2.2', 'django-mjml', 'sendgrid'],
    zip_safe=False,
    license='BSD License',

    packages=find_packages(exclude=['tests*']),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
    ],
)
