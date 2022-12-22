import unittest
import handbrake

class TestStringMethods(unittest.TestCase):

    def test_validfile_returns_true_if_ends_with_ts(self):
        self.assertTrue(handbrake.valid_file("test.ts"))

    def test_validfile_returns_false_if_ends_not_in_ts(self):
        self.assertFalse(handbrake.valid_file("test.mkv"))
        self.assertFalse(handbrake.valid_file("test.mp4"))


if __name__ == '__main__':
    pass
    #unittest.main()