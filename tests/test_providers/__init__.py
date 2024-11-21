"""

"""

import inspect
import unittest
from codetocad.providers import get_provider

from codetocad import *
from codetocad.codetocad_types import *


class TestProviderCase(unittest.TestCase):
    def setUp(self) -> None:

        # Check if the interface is already injected into providers
        # otherwise, use the sample provider
        interface_name = self.__class__.__name__.replace("Test", "_interface").lower()
        interface_name_camelcase = self.__class__.__name__.replace("Test", "Interface")

        interfaces = __import__("codetocad").interfaces
        interface_module = getattr(interfaces, interface_name)
        interface_class = getattr(interface_module, interface_name_camelcase)

        try:
            print("Using provider:", get_provider(interface_class))
        except:
            print("Using sample provider")
            from providers.sample.register import register

            register()

        super().setUp()
