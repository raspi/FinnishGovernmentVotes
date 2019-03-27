# -*- encoding: utf8 -*-

import logging
import os
from main import __VERSION__, __AUTHOR__


from setuptools import find_packages
from setuptools import setup

log = logging.getLogger(__name__)

here = os.path.abspath(os.path.dirname(__file__))
version_file = os.path.join(here, "VERSION")

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.6",
    "Operating System :: POSIX :: Linux",
]

requires = [
    'requests',
    'requests-cache',
    'beautifulsoup4',
]

entry_points = """
"""

tests_require = [
]

testing_extras = tests_require + [
    'nose',
    'coverage',
    'virtualenv',
]

setup(author=__AUTHOR__,
      name='FinnishGovernmentVotes',
      version=__VERSION__,
      description='',
      long_description='',
      classifiers=classifiers,
      author_email='',
      url='https://github.com/raspi/FinnishGovernmentVotes',
      license='Apache 2.0',
      keywords='python finnish government vote votes',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      extras_require={
          'testing': testing_extras,
      },
      tests_require=tests_require,
      #test_suite="tests",
      entry_points=entry_points,
      )