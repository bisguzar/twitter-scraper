#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 기억할 것: 이 파일에서 업로드 기능을 사용하려면, 다음을 해야한다:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

# 메타 데이터의 패키지.
NAME = 'twitter-scraper'
DESCRIPTION = 'Scrape the Twitter Frontend API without authentication.'
URL = 'https://github.com/bisguzar/twitter-scraper'
EMAIL = 'ben@bisguzar.com'
AUTHOR = 'Bugra Isguzar' # Kenneth Reitz가 만듬.
VERSION = '0.2.1'

# 이 함수가 실행되려면 어떤 패키지가 설치되어야 하는가?
REQUIRED = [
    'requests-html',
    'MechanicalSoup'
]

# 나머지는 건드릴 필요 없다
# ------------------------------------------------
# 라이선스와 and Trove Classifiers에 관련된 경우를 제외하고!
# 만약 라이선스를 바꾼다면, 이에 대해 Trove Classifier 역시 바꿔야 한다는 점을 기억하라!

here = os.path.abspath(os.path.dirname(__file__))

# 리드미를 설치하고 long-description으로 이용하라.
# 기억할 것: MANIFEST.in 파일에 'README.rst'가 있을 때만 작동할 것이다!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class UploadCommand(Command):
    """지원 setup.py 업로드."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """글자체를 굵게 출력하."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


# 이 부분이 신기하다:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*", "dist", "*.egg-info"]),

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # 전체 리스트 참고: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py 이 나옴을 지원.
    cmdclass={
        'upload': UploadCommand,
    },
)
