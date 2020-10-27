import unittest


class TestStringMethods(unittest.TestCase):
    def test_isupper(self):
        self.assertTrue('CHANNELNAME'.isupper())
        self.assertFalse('channelname'.isupper())


if __name__ == '__main__':
    unittest.main()
