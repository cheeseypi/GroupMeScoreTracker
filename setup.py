from setuptools import setup

setup(
    name='GroupMeScoreTracker',
    version='1.5',
    url='https://github.com/cheeseypi/GroupMeScoreTracker',
    download_url='https://github.com/cheeseypi/GroupMeScoreTracker/archive/v1.5.tar.gz',
    author='Matthew Doto',
    author_email='matt@mattdoto.com',
    packages=['scoretracker'],
    license='LICENSE.txt',
    description='A score tracker for GroupMe, allowing competition between friends',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True
)
