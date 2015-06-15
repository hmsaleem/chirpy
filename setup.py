import os
import sys
import re, uuid
from distutils.core import setup
from setuptools import setup
from setuptools.command.install import install
from pip.req import parse_requirements

install_reqs = parse_requirements('requirements.txt', session=uuid.uuid1())
reqs = [str(req.req) for req in install_reqs]

class MyInstall(install):

    def run(self):
        install.run(self)
        os.system('python src/chirpy/configModule.py')

setup(
        name = 'chirpy',
        version = '1.0',
        scripts = ['scripts/chirpy'],
        packages = ['chirpy'],
        package_dir = { 'chirpy': 'src/chirpy/'},
        cmdclass={'install': MyInstall},
	install_requires=reqs,
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
	keywords='twitter',


        # project metadata
        author = 'Haji Mohammad Saleem',
        author_email = 'haji.saleem@mail.mcgill.ca',
        description = 'chirpy is a command line interface for quickly collecting and parsing Twitter data.',
        license = 'MIT',
)
