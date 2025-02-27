import unittest


class CustomTestCase(unittest.TestCase):
    def assertEqualTraceless(self, first, second, msg=None):
        try:
            self.assertEqual(first, second, msg)
        except AssertionError as e:
            print(f"Assertion failed: {first} != {second} | Msg: {msg}")

    def assertTrueTraceless(self, first, msg=None):
        try:
            self.assertTrue(first, msg)
        except AssertionError as e:
            print(f"Assertion failed: {first} | Msg: {msg}")

    def assertFalseTraceless(self, first, msg=None):
        try:
            self.assertFalse(first, msg)
        except AssertionError as e:
            print(f"Assertion failed: {first} | Msg: {msg}")
    
    def assertGreaterTraceless(self, first, second, msg=None):
        try:
            self.assertGreater(first, second, msg)
        except AssertionError as e:
            print(f"Assertion failed: {first} <= {second} | Msg: {msg}")
