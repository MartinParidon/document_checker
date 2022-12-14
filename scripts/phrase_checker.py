import sys
import csv
import os
import re
import common
import argparse


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
    try:
        text_ut_path = argv[0].replace('\\', '/')
        out_dir = argv[1].replace('\\', '/')
        phrases_path = argv[2].replace('\\', '/')
        words_path = argv[3].replace('\\', '/')
    except Exception as e:
        print('You didn\'t provide all necessary input params.\n' + str(e))
        sys.exit()
    if os.path.exists(text_ut_path) and os.path.exists(phrases_path) and os.path.exists(words_path):
        text_ut_ext = os.path.splitext(text_ut_path)[1]
        phrases_path_ext = os.path.splitext(phrases_path)[1]
        words_path_ext = os.path.splitext(words_path)[1]
        if text_ut_ext.replace('.', '') not in common.supported_extensions_global:
            print('Check your doc input path extensions.\nText under test must be pdf, dox or doc (very old doc files might not work).')
            sys.exit()
        elif not (phrases_path_ext == '.csv'):
            print('Phrase list not csv format.')
            sys.exit()
        elif not (words_path_ext == '.csv'):
            print('Word list not csv format.')
            sys.exit()
        else:
            return text_ut_path, out_dir, phrases_path, words_path
    else:
        print('Check if all your input paths are valid.')
        sys.exit()


def extract_words_only_from_string(full_text_ut):
    words_list = re.split(' |\n', full_text_ut)
    signs_to_delete = [',', '.', '-', '_', '???', ':', '(', ')', '[', ']']
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
    text_path, out_dir, phrases_path, words_path = input_handling(argv)

    # Make output directory
    # TODO consolidate with plag checker
    try:
        os.makedirs(out_dir, exist_ok=True)
    except Exception as e:
        print('Error making output path.')
        sys.exit()

    # Fetch full text of file in local string
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
    write_count_dict(out_dir + '/phrases.csv', phrases_dict)
    write_count_dict(out_dir + '/words.csv', words_dict)

    # Write console output
    console_out(phrases_dict, words_dict, len(single_words_within_txt_ut))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Test a text document for excessive use of words or phrases that should be avoided')
    parser.add_argument('doc', help='Path to document under test')
    parser.add_argument('out', help='Path to output folder')
    parser.add_argument('phrases', help='Link to phrases csv file that shall be tested')
    parser.add_argument('words', help='Link to words csv file that shall be tested')
    args = parser.parse_args()
    main(sys.argv[1:])
