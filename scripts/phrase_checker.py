import sys
import docx2txt
import csv
import os
from PyPDF2 import PdfReader
import re


def get_count(csv_path, in_list_OR_string):
    in_list = get_list_from_csv_first_row(csv_path)
    out_dict = dict.fromkeys(in_list)
    for elem_ut in in_list:
        out_dict[elem_ut] = in_list_OR_string.count(elem_ut)
    return out_dict


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
    text_path = argv[0].replace('\\', '/')
    phrasen_path = argv[1].replace('\\', '/')
    woerter_path = argv[2].replace('\\', '/')

    # TODO sanity checks and stuff
    text_ext = os.path.splitext(text_path)[1]
    phr_ext = os.path.splitext(phrasen_path)[1]
    w_ext = os.path.splitext(woerter_path)[1]
    if not (text_ext == '.pdf' or text_ext == '.doc' or text_ext == '.docx'):
        print('Input File neither doc, nor docx, nor pdf.')
        quit()
    if not (phr_ext == '.csv' and w_ext == '.csv'):
        print('One or all list files not csv format.')
        quit()

    return text_path, phrasen_path, woerter_path


def prepare_words_list(words_list):
    signs_to_delete = [',', '.', '-', '_', '–', ':', '(', ')', '[', ']']
    words_filtered = []
    for sign in signs_to_delete:
        words_list = list(filter((sign).__ne__, words_list))
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


def get_text_and_wordlist_ut(text_path):
    txt_file_ext = text_path.split('.')[-1]
    if (txt_file_ext == 'doc') or (txt_file_ext == 'docx'):
        full_text_ut = docx2txt.process(text_path)
    elif txt_file_ext == 'pdf':
        reader = PdfReader(text_path)
        full_text_ut = ""
        for page in reader.pages:
            full_text_ut += page.extract_text() + " "
    # ...else... Rest should be filtered out by input treatment!

    words_list_raw = re.split(' |\n', full_text_ut)
    words_list_ut = prepare_words_list(words_list_raw)
    return full_text_ut, words_list_ut


def make_dir_with_id(text_path):
    ID = text_path.split('/')[-1].split('.')[0]
    out_dir = os.getcwd() + '/out/' + ID
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def console_out(phrasen_dict, woerter_dict, word_count):
    ratio_bad_words_ph = round((sum(woerter_dict.values()) / word_count) * 100, 2)
    ratio_bad_phrases_ph = round((sum(phrasen_dict.values()) / word_count) * 100, 2)
    print('Bad phrases ratio: {} per houndred words.'.format(str(ratio_bad_phrases_ph)))
    print('Bad word ratio: {} per houndred words.'.format(str(ratio_bad_words_ph)))
    print('Favourite bad phrase: \"{}\", used {} times.'.format(str(max(phrasen_dict, key=phrasen_dict.get)), str(max(phrasen_dict.values()))))
    print('Favourite bad word: \"{}\", used {} times.'.format(str(max(woerter_dict, key=woerter_dict.get)), str(max(woerter_dict.values()))))


def main(argv):
    text_path, phrasen_path, woerter_path = input_handling(argv)

    out_dir = make_dir_with_id(text_path)

    full_text_ut, words_list_ut = get_text_and_wordlist_ut(text_path)

    phrasen_dict = get_count(phrasen_path, full_text_ut)
    woerter_dict = get_count(woerter_path, words_list_ut)

    write_count_dict(out_dir + '/phrases.csv', phrasen_dict)
    write_count_dict(out_dir + '/words.csv', woerter_dict)

    console_out(phrasen_dict, woerter_dict, len(words_list_ut))


if __name__ == "__main__":
    main(sys.argv[1:])
