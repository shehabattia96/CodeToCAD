import unittest
import tests.test_providers.sample_implemented as sample_implemented

try:
    unittest.main(argv=["-v", "sample_implemented.WireTest"], exit=False)
except Exception as e:
    print(e)
