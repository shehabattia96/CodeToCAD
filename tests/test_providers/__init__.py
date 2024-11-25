import unittest
from codetocad.providers import get_provider

from codetocad import *
from codetocad.codetocad_types import *


def _clear_document():
    """
    This is temporary, we need to replace this with some native method like undo
    or clear document.
    In the meantime, we only have the Blender integration to worry about,
    so this will be hard-coded here:
    """
    try:
        import bpy

        bpy.ops.wm.revert_mainfile()
    except:
        ...


class TestProviderCase(unittest.TestCase):

    def setUp(self) -> None:
        print(f"\nRunning test: {self._testMethodName}")

        _clear_document()

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
