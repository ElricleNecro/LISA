#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pkgutil
from .processor_types import EventProcessor

__all__ = ["EventType"]

# allow automatic loading of modules recursively (automatic registration of
# plugins and viewers)
__path__ = pkgutil.extend_path(__path__, __name__)
for importer, modname, ispkg in pkgutil.walk_packages(
    path=__path__,
    prefix=__name__ + '.'
):
    __import__(modname)

# vim: set tw=79 :
