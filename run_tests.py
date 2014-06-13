import unittest

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suite = loader.discover('tests')
    unittest.TextTestRunner(verbosity=2).run(suite)
