#!/usr/bin/env python

import os, sys
from distutils.core import setup

sys.path.insert(0, os.getcwd())

import mitaka

pkgd = []
for dp, dn, fn in os.walk("mitaka/static"):
    for f in fn:
        pkgd.append(os.path.join(dp, f)[7:])
for dp, dn, fn in os.walk("mitaka/templates"):
    for f in fn:
        pkgd.append(os.path.join(dp, f)[7:])

setup(name="mitaka",
      version=mitaka.__version__,
      author_email="kurin@delete.org",
      author="Toby",
      url="https://github.com/kurin/mitaka",
      package_data={'mitaka': pkgd},
      packages=['mitaka'])

