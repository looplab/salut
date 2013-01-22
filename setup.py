# Copyright 2012 Loop Lab
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup
from salut import __version__


setup(
    name='salut',
    version=__version__,
    py_modules=['salut'],

    install_requires=['pybonjour'],

    tests_require=['nose'],
    test_suite='nose.collector',

    author='Max Persson',
    author_email='max@looplab.se',
    description='Gevent based wrapper for pybonjour',
    license='Apache License 2.0',
    url='https://github.com/looplab/salut',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Networking'
    ],
)
