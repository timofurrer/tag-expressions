# -*- coding: utf-8 -*-

import ast
import os
import codecs
from setuptools import setup, find_packages

"""
Package to parse logical tag expressions
"""

PROJECT_ROOT = os.path.dirname(__file__)


class VersionFinder(ast.NodeVisitor):
    def __init__(self):
        self.version = None

    def visit_Assign(self, node):
        try:
            if node.targets[0].id == 'version':
                self.version = node.value.s
        except:
            pass


def read_version():
    """Read version from tagexpressions/__init__.py without loading any files"""
    finder = VersionFinder()
    path = os.path.join(PROJECT_ROOT, 'tagexpressions', '__init__.py')
    with codecs.open(path, 'r', encoding='utf-8') as fp:
        file_data = fp.read().encode('utf-8')
        finder.visit(ast.parse(file_data))

    return finder.version


def local_text_file(*f):
    path = os.path.join(PROJECT_ROOT, *f)
    with open(path, 'rt') as fp:
        file_data = fp.read()

    return file_data


def read_readme():
    """Read README content.
    If the README.rst file does not exist yet
    (this is the case when not releasing)
    only the short description is returned.
    """
    try:
        return local_text_file('README.rst')
    except IOError:
        return __doc__


setup(name='tag-expressions',
      version=read_version(),
      description=__doc__,
      long_description=read_readme(),
      url='http://github.com/timofurrer/tag-expressions',
      author='Timo Furrer',
      author_email='tuxtimo@gmail.com',
      include_package_data=True,
      packages=find_packages(exclude=['*tests*']),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development :: Testing'
      ]
)
