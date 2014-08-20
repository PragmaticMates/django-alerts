#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-alerts',
    version='0.3.3',
    description='Django alerts',
    long_description=open('README.rst').read(),
    author='Pragmatic Mates',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/django-alerts',
    packages=[
        'alerts',
        'alerts.templatetags',
        'alerts.migrations'
    ],
    include_package_data=True,
    install_requires=('django', ),
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 3 - Alpha'
    ],
    license='BSD License',
    keywords = "django alerts notifications",
)
