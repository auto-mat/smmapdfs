import os
from setuptools import setup, find_packages
import sys
import subprocess

here = os.path.abspath(os.path.dirname(__file__))
import codecs

requires = ['Django']

version = subprocess.check_output(['git','describe','--abbrev=0','--tags']).decode("utf-8")

setup(
        name='django-smmapdfs',
        version=version,
        author='Timothy Hobbs',
        author_email='timothy.hobbs@auto-mat.cz',
        url='https://github.com/auto-mat/smmapdfs',
        download_url="http://pypi.python.org/pypi/django-smmapdfs/",
        description="Generate PDFs from django models by overlaying text onto an existing pdf",
        long_description=codecs.open(
            os.path.join(
                here, 'README.rst'), 'r', 'utf-8').read(),
        license='LPGL, see LICENSE file.',
        install_requires=[
                'django-colorfield',
        ],
        packages=find_packages(),
        include_package_data=True,
        zip_safe=False,
        classifiers=['Topic :: Utilities',
                     'Natural Language :: English',
                     'Operating System :: OS Independent',
                     'Intended Audience :: Developers',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5'],
)
