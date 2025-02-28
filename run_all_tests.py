import unittest
import os
import sys


def discover_and_run_tests():
    test_dir = os.path.dirname(os.path.abspath(__file__))

    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.endswith("_tests.py"):
                rel_path = os.path.relpath(os.path.join(root, file), test_dir)
                module_name = rel_path.replace(os.sep, ".").rsplit(".", 1)[0]

                try:
                    module = __import__(module_name, fromlist=["."])
                    test_suite.addTests(test_loader.loadTestsFromModule(module))

                except Exception as e:
                    print(f"Error loading {module_name}: {e}")
    
    test_runner = unittest.TextTestRunner(verbosity=1)
    result = test_runner.run(test_suite)

    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    discover_and_run_tests()
