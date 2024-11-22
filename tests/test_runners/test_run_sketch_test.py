import unittest
import tests.test_providers.sample_implemented as sample_implemented

try:
    unittest.main(argv=["-v", "sample_implemented.SketchTest"], exit=False)
except Exception as e:
    print(e)
