import sys
import os

sys.path.append(os.path.dirname(sys.path[0]) + '/scripts')

import common
import phrase_checker


def test_get_list_from_csv_first_row():
    result = phrase_checker.get_list_from_csv_first_row("test.csv")
    assert(result == ['test0 test1', 'test2', 'test3'])


def test_get_count_0():
    result = phrase_checker.get_count_in_list(['substring', 'after'], ['This', 'is', 'a', 'test', 'including', 'substring', 'after', 'substring'])
    assert(result == {'substring': 2, 'after': 1})


def test_get_count_1():
    result = phrase_checker.get_count_in_list(['substring', 'after', 'Hessen'], ['This', 'is', 'a', 'test', 'including', 'subst ring', 'after', 'substring'])
    assert(result == {'substring': 1, 'after': 1, 'hessen': 0})


def test_get_count_2():
    result = phrase_checker.get_count_in_string(['the thIrd', 'no means'], 'By no means do I believe that no means not no but no always means no. THIS IS THE THIRD TIME I\'M TELLING YOU THIS')
    assert(result == {'no means': 2, 'the third': 1})


def test_get_string_from_path_0():
    result = common.get_string_from_path('testfile_0.docx')
    assert(result == 'This is text string of file testfile_0.docx')


# TODO Doc support
#def test_get_string_from_path_1():
#    result = common.get_string_from_path('testfile_1.doc')
#    assert(result == 'This is text string of file testfile_1.doc')


# TODO better PDF support lib?!
#def test_get_string_from_path_2():
#    result = common.get_string_from_path('testfile_2.pdf')
#    assert(result == 'This is text string of file testfile_2.pdf')


def test_get_string_from_path_3():
    result = common.get_string_from_path('testfile_3.txt')
    assert(result == 'This is text string of file testfile_3.txt')
