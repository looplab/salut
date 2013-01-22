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


execfile('salut/version.py')


from setuptools import setup


setup(
    name=__title__,
    version=__version__,
    packages=['salut'],

    install_requires=['gevent', 'pybonjour'],

    tests_require=['nose'],
    test_suite='nose.collector',

    author=__author__,
    author_email='max@looplab.se',
    description='Gevent based wrapper for pybonjour',
    license=__license__,
    url=__project_url__,
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
