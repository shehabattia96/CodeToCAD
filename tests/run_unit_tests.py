import unittest
import tests.test_providers.sample_implemented as sample_implemented

"""
To run this, import it into the software or run `codetocad tests_integration/run_unit_tests.py`

To run a specific method, use `unittest.main(argv=["-v", "sample_implemented.PartTest.test_create_cube"], exit=False)` instead.
"""

try:
    unittest.main(sample_implemented, exit=False, argv=["-v"])
except Exception as e:
    print(e)
