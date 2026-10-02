import unittest, sys, os

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath("."))

if __name__ == "__main__":
    loader = unittest.TestLoader()
    suite = loader.discover("tests", pattern="test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\n✅ ALL ENTERPRISE AI PLATFORM TESTS PASSED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print(f"\n❌ TEST FAILURES DETECTED: {len(result.failures)} failures, {len(result.errors)} errors")
        sys.exit(1)
