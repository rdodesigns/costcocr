from setuptools import setup

import sys
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


def readme():
    with open('README.md') as f:
        return f.read()

setup( name             = 'costcocr'
     , version          = '0.0.1'
     , description      = 'Costco Receipt OCR'
     , long_description = readme()
     , keywords         = [ 'Costco', 'OCR']
     , author           = 'Matt Adams and Ryan Orendorff'
     , author_email     = 'ryan@rdodesigns.com'
     , license          = 'BSD'
     , classifiers      =
        [ 'Development Status :: 1 - Planning'
        , 'License :: OSI Approved :: BSD License'
        , 'Programming Language :: Python'
        ]
     , packages         = ['costcocr']
     , install_requires =
        [ 'six >= 1.6'
        ]
     , zip_safe         = False
     , tests_require    = ['pytest']
     , cmdclass         = {'test': PyTest}
     )

