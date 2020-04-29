import unittest
from classes.core import IssueCollector


class TestIssueCollector(unittest.TestCase):

    def test_search(self):
        result = IssueCollector.search('project=TEST')
        self.assertIn('TEST', str(result))


if __name__ == '__main__':
    unittest.main()