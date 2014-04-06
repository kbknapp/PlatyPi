import sys
from distutils.core import setup, Extension


pp_ext = Extension(
    'platypi',
    include_dirs=['/usr/include/platypi/'],
    libraries=[],
    library_dirs=['/usr/lib'],
    sources=[]
)

setup(
    name='platypi',
    version='0.1',
    description='Controller for the PlatyPi',
    author='Kevin Knapp',
    author_email='kbknapp@gmail.com',
    license='GPLv2',
    url='https://github.com/kbknapp/PlatyPi',
    ext_modules=[pp_ext],
    long_description=open('README.md').read() + open('CHANGELOG').read(),
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v2 or "
        "later (AGPLv2)",
        "Programming Language :: Cython",
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='raspberrypi',
)
