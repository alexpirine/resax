#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
        name='Django-ResaX',
        version='1.1',
        url='https://github.com/alexpirine/resax',
        license='New BSD License',
        author='Alexandre Syenchuk',
        author_email='as@netica.fr',
        description='Django API for reservation systems',
        packages=['resax'],
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'Django >= 1.10',
            'swapper >= 1.0.0',
        ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Framework :: Django :: 1.9',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.5',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Libraries :: Application Frameworks',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
