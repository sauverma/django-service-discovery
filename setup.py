from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='dab_servdisco',
      version=version,
      description="Django consul-based service discovery and service invocation",
      long_description="""\
Django consul-based service discovery and service invocation""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='sauverma',
      author_email='saurabhdec1988@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
