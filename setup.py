#!/usr/bin/env python

from distutils.core import setup

setup(name='IDLSave',
      version='1.0.0',
      description='IDLSave - a module to read IDL save files into Python',
      author='Thomas Robitaille',
      author_email='thomas.robitaille@gmail.com',
      url='https://github.com/astrofrog/idlsave',
      packages=['idlsave'],
      provides=['idlsave'],
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 5 - Production/Stable",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
