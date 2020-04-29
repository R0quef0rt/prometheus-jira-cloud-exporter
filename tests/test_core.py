import unittest
from classes.core import IssueCollector


class TestIssueCollector(unittest.TestCase):

    def test_construct(self):
        out = IssueCollector.construct('project=TEST')
        self.assertIn('TEST', str(out))


if __name__ == '__main__':
    unittest.main()