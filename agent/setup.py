#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Installation script for the Coral Agent.
"""

from pathlib import Path
from setuptools import setup, find_packages


def check_cwd():
    """
    You must always change directory to the parent of this file before
    executing the setup.py script. If not setuptools will fail reading files,
    including and excluding files from the MANIFEST.in, defining the library
    path, etc.
    """
    from os import chdir

    here = Path(__file__).resolve().parent
    if Path().cwd().resolve() != here:
        print('Changing directory to {}'.format(here))
        chdir(str(here))


check_cwd()


def read(filename):
    """
    Read the content of a file.

    :param str filename: The file to read.

    :return: The content of the file.
    :rtype: str
    """
    return Path(filename).read_text(encoding='utf-8')


def find_version(filename):
    """
    Find version of a package.

    This will read and parse a Python module that has defined a __version__
    variable. This function does not import the file.

    ::

        setup(
            ...
            version=find_version('lib/package/__init__.py'),
            ...
        )

    :param str filename: Path to a Python module with a __version__ variable.

    :return: The version of the package.
    :rtype: str
    """
    import re

    content = read(filename)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M
    )
    if not version_match:
        raise RuntimeError('Unable to find version string.')

    version = version_match.group(1)

    print('Version found:')
    print('  {}'.format(version))
    print('--')

    return version


def find_requirements(filename):
    """
    Finds PyPI compatible requirements in a pip requirements.txt file.

    In this way requirements needs to be specified only in one, centralized
    place:

    ::

        setup(
            ...
            install_requires=find_requirements('requirements.txt'),
            ...
        )

    Supports comments and non PyPI requirements (which are ignored).

    :param str filename: Path to a requirements.txt file.

    :return: List of requirements with version.
    :rtype: list
    """
    import string

    content = read(filename)
    requirements = []
    ignored = []

    for line in (
        line.strip() for line in content.splitlines()
    ):
        # Comments
        if line.startswith('#') or not line:
            continue

        if line[:1] not in string.ascii_letters:
            ignored.append(line)
            continue

        requirements.append(line)

    print('Requirements found:')
    for requirement in requirements:
        print('  {}'.format(requirement))
    print('--')

    print('Requirements ignored:')
    for requirement in ignored:
        print('  {}'.format(requirement))
    print('--')

    return requirements


setup(
    name='coral_agent',
    version=find_version('coral_agent/__init__.py'),
    packages=find_packages(),

    # Dependencies
    install_requires=find_requirements('requirements.txt') + [
        '{}; platform_system == "Windows"'.format(requirement)
        for requirement in find_requirements('requirements.windows.txt')
    ],

    # Data files
    package_data={
        'coral_agent': [
            'data/*',
        ],
    },

    # Metadata
    author='KuraLabs S.R.L',
    author_email='info@kuralabs.io',
    description=(
        'Agent (data collector) for the Coral Project (Gaming PC)'
    ),
    long_description=read('README.rst'),
    url='https://github.com/kuralabs/coral-dashboard',
    keywords='coral_agent',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Microsoft :: Windows :: Windows 10',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires='>=3.5.0',

    # Entry points
    entry_points={
        'console_scripts': [
            'coral_agent = coral_agent.__main__:main',
        ],
        'coral_agent_builds_1_0': [
            'coral = coral_agent.builds.coral:CoralAgent',
        ],
    },
)
