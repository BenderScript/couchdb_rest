from setuptools import setup
import sys
import pip
import os

with open(os.path.join(os.path.dirname(__file__), '__init__.py')) as version_file:
    exec(version_file.read())

if sys.version_info < (3, 6, 3):
    sys.exit("Sorry, you need Python 3.6.3+")

pip_version = int(pip.__version__.replace(".", ""))
if pip_version < 901:
        sys.exit("Sorry, you need pip 9.0.1+")

setup(
    name='couchdb_rest_api',
    version=__version__,
    description='CouchDB REST API',
    long_description='Wrapper around the couchdb REST API',
    install_requires=[
        'coverage>=4.5.1',
        'docker>=3.3.0',
        'flake8>=3.3.0',
        'pymongo>=3.4.0',
        'pytest>=3.4.0',
        'responses>=0.5.1',
        'Sphinx>=1.6.3',
        'wheel>=0.30.0a0',
        'magen_logger>=1.0a1',
        'magen_utils>=1.2a2',
        'magen_rest_service>=1.3a10'
      ],
    package_dir={'': '.'},
    packages={'couchdb_rest_apis', 'couchdb_docker_apis'},
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']
    },
    test_suite='tests',
    url='https://magengit.github.io/',
    license='Apache Software License',
    author='Reinaldo Penno',
    author_email='rapenno@gmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 2 - Pre-Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Legal Industry',
        'Topic :: Security',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6',
    ],
)
