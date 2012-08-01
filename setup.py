#!/usr/bin/env python

from distutils.core import setup

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py

setup(name='IDLSave',
      version='0.9.7',
      description='IDLSave - a module to read IDL save files into Python',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      url='https://github.com/astrofrog/idlsave',
      packages=['idlsave'],
      provides=['idlsave'],
      cmdclass={'build_py': build_py},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 5 - Production/Stable",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
