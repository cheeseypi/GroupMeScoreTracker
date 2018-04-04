from setuptools import setup

ver = '1.6'

setup(
    name='GroupMeScoreTracker',
    version=ver,
    url='https://github.com/cheeseypi/GroupMeScoreTracker',
    download_url='https://github.com/cheeseypi/GroupMeScoreTracker/archive/v'+ver+'.tar.gz',
    author='Matthew Doto',
    author_email='matt@mattdoto.com',
    packages=['scoretracker'],
    license='LICENSE.txt',
    description='A score tracker for GroupMe, allowing competition between friends',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True
)
