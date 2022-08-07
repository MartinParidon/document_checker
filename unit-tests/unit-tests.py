import unittest
from scripts import phrase_checker
from scripts import plagiarism_checker


class TestPhraseChecker(unittest.TestCase):
    def get_list_from_csv_first_row__ut_0(self):
        result = phrase_checker.get_list_from_csv_first_row("test.csv")
        self.assertEqual(result, ['test0 test1', 'test2', 'test3'])

    def get_count__ut_0(self):
        result = phrase_checker.get_count(['substring', 'after'], ['This', 'is', 'a', 'test', 'including', 'substring', 'after', 'substring'])
        self.assertEqual(result, {'substring': 2, 'after': 1})

    def get_count__ut_1(self):
        result = phrase_checker.get_count(['substring', 'after', 'Hessen'], ['This', 'is', 'a', 'test', 'including', 'subst ring', 'after', 'substring'])
        self.assertEqual(result, {'after': 1, 'substring': 1, 'Hessen': 0})

    def get_count__ut_2(self):
        result = phrase_checker.get_count(['the third', 'no means'], ['By no means do I believe that no means not no but no always means no. THIS IS THE THIRD TIME I\'M TELLING YOU THIS'])
        self.assertEqual(result, {'no means': 2, 'the third': 1})
