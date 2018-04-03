from setuptools import setup

setup(
    name='GroupMeScoreTracker',
    version='1.1',
    url='https://github.com/cheeseypi/GroupMeScoreTracker',
    download_url='https://github.com/cheeseypi/GroupMeScoreTracker/archive/v1.0.tar.gz',
    author='Matthew Doto',
    author_email='matt@mattdoto.com',
    packages=['scoretracker'],
    license='LICENSE.txt',
    description='A score tracker for GroupMe, allowing competition between friends',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines()
)
