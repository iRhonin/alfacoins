import re
from os.path import join, dirname
from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'alfacoins', '__init__.py')) as v_file:
    package_version = re.\
        compile(r".*__version__ = '(.*?)'", re.S).\
        match(v_file.read()).\
        group(1)


dependencies = [
    'requests'
]


setup(
    name="alfacoins",
    version=package_version,
    author="Arash Fatahzadea",
    author_email="arash.fattahzade@carrene.com",
    description="ALFACoins API library",
    url='https://github.com/Carrene/owl.git://github.com/ArashFatahzade/alfacoins',
    install_requires=dependencies,
    packages=find_packages(),
    test_suite="tests",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
