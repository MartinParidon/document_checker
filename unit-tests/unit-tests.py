import unittest
from scripts import phrase_checker
from scripts import plagiarism_checker


class TestPhraseChecker(unittest.TestCase):
    def test_get_list_from_csv_first_row(self):
        result = phrase_checker.get_list_from_csv_first_row("test.csv")
        self.assertEqual(result, ['test0 test1', 'test2', 'test3'])

    def test_get_count_0(self):
        result = phrase_checker.get_count_in_list(['substring', 'after'], ['This', 'is', 'a', 'test', 'including', 'substring', 'after', 'substring'])
        self.assertEqual(result, {'substring': 2, 'after': 1})

    def test_get_count_1(self):
        result = phrase_checker.get_count_in_list(['substring', 'after', 'Hessen'], ['This', 'is', 'a', 'test', 'including', 'subst ring', 'after', 'substring'])
        self.assertEqual(result, {'substring': 1, 'after': 1, 'hessen': 0})

    def test_get_count_2(self):
        result = phrase_checker.get_count_in_string(['the thIrd', 'no means'], 'By no means do I believe that no means not no but no always means no. THIS IS THE THIRD TIME I\'M TELLING YOU THIS')
        self.assertEqual(result, {'no means': 2, 'the third': 1})


if __name__ == '__main__':
    unittest.main()
