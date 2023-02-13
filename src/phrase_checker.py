# coding: utf-8

import sys
import csv
import os
import re
import common
import phrase_checker_gui
from PySide6 import QtWidgets
import yaml


class MainWindow(QtWidgets.QMainWindow, phrase_checker_gui.Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.input_folder_path = ''
        self.output_folder_path = ''
        self.phrases_file_path = ''
        self.words_file_path = ''
        self.config_file_path = ''
        self.pushButton_input_folder_path.clicked.connect(self.on_pushButton_input_folder_path_clicked)
        self.pushButton_output_folder_path.clicked.connect(self.on_pushButton_output_folder_path_clicked)
        self.pushButton_phrases_file_path.clicked.connect(self.on_pushButton_phrases_file_path_clicked)
        self.pushButton_words_file_path.clicked.connect(self.on_pushButton_words_file_path_clicked)
        self.pushButton_run.clicked.connect(self.on_pushButton_run_clicked)
        if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]) and sys.argv[1].split('.')[-1] == 'yaml':
            self.load_config(sys.argv[1])

    def load_config(self, config_file_path):
        with open(config_file_path, 'r') as stream:
            try:
                config = yaml.safe_load(stream)
                self.input_folder_path = config['input_folder_path']
                self.lineEdit_input_folder_path.setText(self.input_folder_path)
                self.output_folder_path = config['output_folder_path']
                self.lineEdit_output_folder_path.setText(self.output_folder_path)
                self.phrases_file_path = config['phrases_file_path']
                self.lineEdit_phrases_file_path.setText(self.phrases_file_path)
                self.words_file_path = config['words_file_path']
                self.lineEdit_words_file_path.setText(self.words_file_path)
            except yaml.YAMLError as exc:
                print(exc)

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
        with open(self.output_folder_path + '/config.yaml', 'w') as yaml_file:
            yaml.dump({'input_folder_path': self.input_folder_path, 'output_folder_path': self.output_folder_path,
                       'phrases_file_path': self.phrases_file_path, 'words_file_path': self.words_file_path}, yaml_file,
                      default_flow_style=False, allow_unicode=True)
        main([self.input_folder_path, self.output_folder_path, self.phrases_file_path, self.words_file_path])


def get_count_in_list(elements_ut, list_ut):
    elements_ut_lower = [e.lower() for e in elements_ut]
    list_ut_lower = [e.lower() for e in list_ut]
    out_dict = dict.fromkeys(elements_ut_lower)
    for elem_ut in elements_ut_lower:
        out_dict[elem_ut] = list_ut_lower.count(elem_ut)
    return out_dict


# TODO Make sure substring isn't enclosed by chars
def get_count_in_string(elements_ut, string_ut):
    elements_ut_lower = [e.lower() for e in elements_ut]
    string_ut_lower = string_ut.lower()
    out_dict = dict.fromkeys(elements_ut_lower)
    for elem_ut in elements_ut_lower:
        out_dict[elem_ut] = string_ut_lower.count(elem_ut)
    return out_dict


def get_list_from_csv_first_row(csv_file):
    with open(csv_file, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row_1 = next(csvreader)
        row_1_lower = [e.lower() for e in row_1]
    return row_1_lower


def write_count_dict(csv_path, list_of_dicts, text_paths):
    with open(csv_path, 'w', newline='') as csvfile:
        header = list(list_of_dicts[0].keys())
        header.append('text_path')
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for idx, specific_dict in enumerate(list_of_dicts):
            specific_dict['text_path'] = text_paths[idx]
            writer.writerow(specific_dict)


def input_handling(argv):
    # argv = [self.input_folder_path, self.output_folder_path, self.phrases_file_path, self.words_file_path]
    files_to_check = []
    for folder, subs, filenames in os.walk(argv[0]):
        for filename in filenames:
            if not (filename.endswith(".doc") or filename.endswith(".docx") or filename.endswith("pdf") or filename.endswith(".txt")): # ANY (?!)
                continue
            else:
                files_to_check.append(os.path.join(argv[0], os.path.join(folder, filename)))
    if len(files_to_check) == 0:
        print("No files to check")
        sys.exit()
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
    # argv = [self.input_folder_path, self.output_folder_path, self.phrases_file_path, self.words_file_path]
    # If valid, fetch path to text and input list
    text_paths, out_dir, phrases_path, words_path = input_handling(argv)

    # Fetch list of bad phrases from provided csv file
    phrases_list = sorted(get_list_from_csv_first_row(phrases_path))

    # Fetch list of bad words from provided csv file
    words_list = sorted(get_list_from_csv_first_row(words_path))

    # Aggregate bad phrases and words in one dict
    phrases_dicts_list = []
    words_dicts_list = []

    # Fetch full text of file in local string
    for text_path in text_paths:

        full_text_ut = common.get_string_from_path(text_path)

        # Early out if doc empty
        if not full_text_ut:
            print('Error reading file: {}'.format(text_path))
            continue

        # TODO: Check if no 'space' within any entry of list
        # ??

        # Get count of bad phrases as absolute counts within full text
        phrases_counts = get_count_in_string(phrases_list, full_text_ut)
        phrases_dicts_list.append(phrases_counts)

        # Fetch list of individual words within doc ut
        single_words_within_txt_ut = extract_words_only_from_string(full_text_ut)

        # Get count of bad words as absolute counts within list of words
        words_counts = get_count_in_list(words_list, single_words_within_txt_ut)
        words_dicts_list.append(words_counts)

    # Write output dicts to csv
    write_count_dict(out_dir + '/phrases.csv', phrases_dicts_list, text_paths)
    write_count_dict(out_dir + '/words.csv', words_dicts_list, text_paths)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainwindow = MainWindow()
    mainwindow.show()
    sys.exit(app.exec())
