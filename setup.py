import os
import sys
from distutils.core import setup
from setuptools import setup
from setuptools.command.install import install

class MyInstall(install):

    def run(self):
        install.run(self)
        os.system('python src/harvest/configModule.py')

setup(
        name = 'harvest',
        version = '1.0',
        scripts = ['scripts/harvest'],
        packages = ['harvest'],
        package_dir = { 'harvest': 'src/harvest/'},
        cmdclass={'install': MyInstall},
	install_requires=[
        	'twitter==1.14.2',
		'tweepy==2.3.0',
		'configparser==3.3.0r2',
        	'prettytable==0.7.2',
	],
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Science/Research',
		'Intended Audience :: System Administrators',
		'Intended Audience :: Information Technology',
		'Programming Language :: Python :: 2.7',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Topic :: Internet',
		'Operating System :: MacOS',
		'Operating System :: Unix',
	],
	keywords='twitter'


        # project metadata
        author = 'Haji Mohammad Saleem',
        author_email = 'haji.saleem@mail.mcgill.ca',
        description = 'Harvest is a command line interface for quickly collecting and parsing Twitter data.',
        license = 'MIT',
)
