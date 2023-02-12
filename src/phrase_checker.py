import sys
import csv
import os
import re
import common
import phrase_checker_gui
from PySide6 import QtWidgets


class MainWindow(QtWidgets.QMainWindow, phrase_checker_gui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.input_folder_path = ''
        self.output_folder_path = ''
        self.phrases_file_path = ''
        self.words_file_path = ''
        self.pushButton_input_folder_path.clicked.connect(self.on_pushButton_input_folder_path_clicked)
        self.pushButton_output_folder_path.clicked.connect(self.on_pushButton_output_folder_path_clicked)
        self.pushButton_phrases_file_path.clicked.connect(self.on_pushButton_phrases_file_path_clicked)
        self.pushButton_words_file_path.clicked.connect(self.on_pushButton_words_file_path_clicked)
        self.pushButton_run.clicked.connect(self.on_pushButton_run_clicked)

    def on_pushButton_input_folder_path_clicked(self):
        self.input_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                            'Select Input Folder Path',
                                                                            os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        self.lineEdit_input_folder_path.setText(self.input_folder_path)

    def on_pushButton_output_folder_path_clicked(self):
        self.output_folder_path = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                             'Select Output Folder Path',
                                                                             os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
        self.lineEdit_output_folder_path.setText(self.output_folder_path)

    def on_pushButton_phrases_file_path_clicked(self):
        self.phrases_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                          'Select Phrases File Path',
                                                                          os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
                                                                          "(*.csv)")
        self.lineEdit_phrases_file_path.setText(self.phrases_file_path)

    def on_pushButton_words_file_path_clicked(self):
        self.words_file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                           'Select Words File Path',
                                                                           os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'),
                                                                           "(*.csv)")
        self.lineEdit_words_file_path.setText(self.words_file_path)

    def on_pushButton_run_clicked(self):
        main([self.input_folder_path, self.output_folder_path, self.phrases_file_path, self.words_file_path])


def get_count_in_list(elements_ut, list_ut):
    elements_ut_lower = [e.lower() for e in elements_ut]
    list_ut_lower = [e.lower() for e in list_ut]
    out_dict = dict.fromkeys(elements_ut_lower)
    for elem_ut in elements_ut_lower:
        out_dict[elem_ut] = list_ut_lower.count(elem_ut)
    return dict(sorted(out_dict.items(), key=lambda kv: kv[1], reverse=True))


# TODO Make sure substring isn't enclosed by chars
def get_count_in_string(elements_ut, string_ut):
    elements_ut_lower = [e.lower() for e in elements_ut]
    string_ut_lower = string_ut.lower()
    out_dict = dict.fromkeys(elements_ut_lower)
    for elem_ut in elements_ut_lower:
        out_dict[elem_ut] = string_ut_lower.count(elem_ut)
    return dict(sorted(out_dict.items(), key=lambda kv: kv[1], reverse=True))


def get_list_from_csv_first_row(csv_file):
    with open(csv_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_1 = next(csvreader)
    return row_1


def write_count_dict(cv_in, dict_ut):
    with open(cv_in, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=dict_ut.keys())
        writer.writeheader()
        writer.writerows([dict_ut])


def input_handling(argv):
    files_to_check = []
    # TODO is this recursive?
    for file in os.listdir(argv[0]):
        if not (file.endswith(".doc") or file.endswith(".docx") or file.endswith("pdf") or file.endswith(".txt")): # ANY (?!)
            continue
        else:
            files_to_check.append(os.path.join(argv[0], file))
    return files_to_check, argv[1], argv[2], argv[3]


def extract_words_only_from_string(full_text_ut):
    words_list = re.split(' |\n', full_text_ut)
    signs_to_delete = [',', '.', '-', '_', '–', ':', '(', ')', '[', ']']
    words_filtered = []
    for sign in signs_to_delete:
        words_list = list(filter(sign.__ne__, words_list))
    for word in words_list:
        if any(sign in word for sign in signs_to_delete):
            signs_found = [sign for sign in signs_to_delete if sign in word]
            word_to_add = word
            for sign in signs_found:
                word_to_add = word_to_add.replace(sign, '')
            words_filtered.append(word_to_add)
        else:
            words_filtered.append(word)
    words_filtered = [x for x in words_filtered if not (x.isdigit())]
    return words_filtered


def console_out(phrases_dict, words_dict, word_count):
    sorted_keys_phrases = [item[0] for item in phrases_dict.items()]
    sorted_values_phrases = [item[1] for item in phrases_dict.items()]
    sorted_keys_words = [item[0] for item in words_dict.items()]
    sorted_values_words = [item[1] for item in words_dict.items()]
    phrases_ratio = round((sum(phrases_dict.values()) / word_count) * 100, 2)
    words_ratio = round((sum(words_dict.values()) / word_count) * 100, 2)
    print('\n{} bad phrases per houndred words. Favourites:'.format(str(phrases_ratio)))
    for i_word in range(0, 9):
        print('\"{}\": {}'.format(str(sorted_keys_phrases[i_word]), str(sorted_values_phrases[i_word])))
    print('\n{} bad words per houndred words. Favourites:'.format(str(words_ratio)))
    for i_word in range(0, 9):
        print('\"{}\": {}'.format(str(sorted_keys_words[i_word]), str(sorted_values_words[i_word])))


def main(argv):
    # If valid, fetch path to text and input list
    text_paths, out_dir, phrases_path, words_path = input_handling(argv)

    # Fetch full text of file in local string
    for text_path in text_paths:

        # Make output directory
        # TODO consolidate with plag checker
        out_dir_file = os.path.join(out_dir, os.path.basename(text_path))
        try:
            os.makedirs(out_dir_file, exist_ok=True)
        except Exception as e:
            print('Error making output path.')
            sys.exit()

        full_text_ut = common.get_string_from_path(text_path)

        # Early out if doc empty
        if not full_text_ut:
            print('Document under test is empty. Provide link to a document that is not empty.')
            sys.exit()

        # TODO: Check if no 'space' within any entry of list
        # Fetch list of bad phrases from provided csv file
        phrases_list = get_list_from_csv_first_row(phrases_path)

        # Get count of bad phrases as absolute counts within full text
        phrases_dict = get_count_in_string(phrases_list, full_text_ut)

        # Fetch list of bad words from provided csv file
        words_list = get_list_from_csv_first_row(words_path)

        # Fetch list of individual words within doc ut
        single_words_within_txt_ut = extract_words_only_from_string(full_text_ut)

        # Get count of bad words as absolute counts within list of words
        words_dict = get_count_in_list(words_list, single_words_within_txt_ut)

        # Write output dicts to csv
        write_count_dict(out_dir_file + '/phrases.csv', phrases_dict)
        write_count_dict(out_dir_file + '/words.csv', words_dict)

        # Write console output
        console_out(phrases_dict, words_dict, len(single_words_within_txt_ut))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #parser = argparse.ArgumentParser(
    #    description='Test a text document for excessive use of words or phrases that should be avoided')
    #parser.add_argument('doc', help='Path to document under test')
    #parser.add_argument('out', help='Path to output folder')
    #parser.add_argument('phrases', help='Link to phrases csv file that shall be tested')
    #parser.add_argument('words', help='Link to words csv file that shall be tested')
    #args = parser.parse_args()
    #main(sys.argv[1:])

    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
    #mainwindow.show()
    #cfg_file_ext = os.path.splitext(app.lineEdit_input_folder)[1]
    #main(sys.argv[1:])
