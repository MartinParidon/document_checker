import glob
import matplotlib.pyplot as plt
import time
from datetime import datetime
from pyvis.network import Network
import os
import sys
import common
import re
import argparse

debug_on_global = False

# Search n_optimal
best_len_str_search_d_chars_global = 2
best_len_str_search_min_range_global = 10
best_len_str_search_max_range_global = 60

string_to_export_global = ''

in_path_global = ''
out_path_global = ''

default_best_str_global = 40

default_cutoff_global = 0.9


def get_file_paths(root_dir):
    search_patterns_relative = ['/**/*.' + ext for ext in common.supported_extensions_global]
    search_patterns_absolute = []
    for type_iter in search_patterns_relative:
        search_patterns_absolute.append(root_dir + type_iter)
    files_grabbed = []
    for files in search_patterns_absolute:
        files_grabbed.extend(glob.glob(files, recursive=True))
    file_paths = []
    [file_paths.append(file_grabbed.replace('\\', '/')) for file_grabbed in files_grabbed]
    my_print(file_paths)
    return file_paths


def read_text_strings(files_ut_paths):
    full_text_ut_list = []
    files_ut_paths_to_remove = []
    for i_path, text_path in enumerate(files_ut_paths):
        my_print('\n\n')
        full_text_raw = common.get_string_from_path(text_path)
        if full_text_raw is not None:
            my_print('file: ' + str(i_path) + ', path: ' + files_ut_paths[i_path] + ': \n' + full_text_raw)
            full_text_ut_list.append(full_text_raw)
        else:
            files_ut_paths_to_remove.append(text_path)
    files_ut_paths_cleaned = [files_ut_path for files_ut_path in files_ut_paths if files_ut_path not in files_ut_paths_to_remove]
    return full_text_ut_list, files_ut_paths_cleaned


def my_print(str_to_print, show_output=False):
    global string_to_export_global
    if debug_on_global or show_output:
        print(str_to_print)
        string_to_export_global = string_to_export_global + '\n' + str(str_to_print)


def find_i_subs(text_strings_full, files_ut_paths, is_testrun, substring_len):
    show_output = not is_testrun
    files_ut_paths_clean = files_ut_paths
    text_strings_l2 = text_strings_full
    n_subs = 0
    # https://towardsdatascience.com/pyvis-visualize-interactive-network-graphs-in-python-77e059791f01
    # https://pyvis.readthedocs.io/en/latest/documentation.html
    if not is_testrun:
        edges = []
        net = Network(height='100%', width='70%')
        net.barnes_hut()
    for i_file, text_string_full_ut in enumerate(text_strings_full):
        my_print('\n' + str(files_ut_paths[i_file]), show_output)
        substrings = []
        [substrings.append(text_string_full_ut[i:i + substring_len]) for i in range(0, len(text_string_full_ut), substring_len) if (len(text_string_full_ut[i:i + substring_len]) == substring_len)]
        text_strings_l2 = text_strings_l2[1:]
        files_ut_paths_clean = files_ut_paths_clean[1:]
        for i_found_file, text_string_l2_ut in enumerate(text_strings_l2):
            subs_found = []
            for substring in substrings:
                if substring in text_string_l2_ut:
                    my_print('\'' + substring.replace('\n', ' ') + '\'' + ' also found in ' + files_ut_paths_clean[i_found_file], show_output)
                    subs_found.append(substring)
                    n_subs = n_subs + 1
            if not is_testrun:
                if len(subs_found) > 0:
                    net.add_node(files_ut_paths[i_file])
                    net.add_node(files_ut_paths_clean[i_found_file])
                    edges.append((files_ut_paths[i_file], files_ut_paths_clean[i_found_file], len(subs_found)))
    my_print('\nSubstrings found: ' + str(n_subs), show_output)
    if not is_testrun:
        net.add_edges(edges)
        net.show_buttons(filter_=['physics'])
        net.show(out_path_global + '/graph.html')
    return n_subs


def save_figure(x, y, x_base, y_diff):
    global out_path_global
    global default_cutoff_global
    plt.subplots()
    plt.plot(x, y, '*')
    plt.savefig(out_path_global + '/plagiarism_analysis_x_y')
    plt.subplots()
    plt.plot(x_base, y_diff, x_base, [default_cutoff_global] * len(y_diff))
    plt.savefig(out_path_global + '/plagiarism_analysis_x_ydiff')


def find_best_str_len(text_strings_full, files_ut_paths):
    global default_best_str_global
    global default_cutoff_global
    substring_lengths = {}
    for _, i_len in enumerate(range(best_len_str_search_min_range_global, best_len_str_search_max_range_global, best_len_str_search_d_chars_global)):
        my_print('substring len: ' + str(i_len))
        substring_lengths[i_len] = find_i_subs(text_strings_full, files_ut_paths, True, i_len)
    lists = sorted(substring_lengths.items())
    x, y = zip(*lists)
    y_diff = [i / j if j > 0 else 1 for i, j in zip(y[1:], y[:-1])]
    x_base = x[1:]
    try:
        best_str_len = min([x_ for x_, y_ in zip(x_base, y_diff) if y_ > default_cutoff_global])
        my_print('Best string length found: ' + str(best_str_len), show_output=True)
    except Exception as e:
        best_str_len = default_best_str_global
        my_print('Error finding best string. Outputting default.', show_output=True)
    save_figure(x, y, x_base, y_diff)
    return best_str_len


def delete_citations_in_texts(text_strings_full):
    text_strings_filtered = []
    for text_str in text_strings_full:
        # Verified with https://regex101.com/r/hsASKA/1
        # Hard coded for now: "(SURNAME, YYYY, Page)"
        citation_regex = re.compile(r"(\(.*,\s(\d|[1-9]\d|[1-9]\d\d|[1-2]\d\d\d),\sS\.\s(\d|[1-9]\d|[1-9]\d\d|[1-9]\d\d\d|[1-9]\d\d\d\d)\))")
        citation_occurrences = re.findall(citation_regex, text_str)
        for cit_occ in citation_occurrences:
            text_str = text_str.replace(cit_occ[0], '')
        text_strings_filtered.append(text_str)
    return text_strings_filtered


def delete_bibliography(text_strings_full):
    text_strings_filtered = []
    num_correct_citations = []
    for text_str in text_strings_full:
        # https://regex101.com/r/ylDKB4/1
        # https://www.beltz.de/fileadmin/beltz/downloads/Manuskripthinweise.pdf
        citation_regex = re.compile(r".*,.*?\((\d|[1-9]\d|[1-9]\d\d|[1-9]\d\d\d)\)\.\s.*?\..*\.")
        text_strings_filtered.append(re.sub(citation_regex, '', text_str))
        num_correct_citations.append(len(re.findall(citation_regex, text_str)))
    return text_strings_filtered, num_correct_citations


def main(input_args):
    # Start timer
    start_time = round(time.perf_counter(), 2)

    # Python...
    global out_path_global
    global default_best_str_global
    global string_to_export_global

    # Flush output string
    string_to_export_global = ''

    # TODO Implement...
    # https://stackoverflow.com/questions/9532499/check-whether-a-path-is-valid-in-python-without-creating-a-file-at-the-paths-ta
    # Set output path according to given input path name. Then print
    in_path = input_args[0]

    # Make out path
    out_path_global = input_args[1]
    try:
        os.makedirs(out_path_global, exist_ok=True)
    except Exception as e:
        my_print('Error making output path.', show_output=True)
        sys.exit()

    # Infos
    my_print('\nTesting: ' + in_path, show_output=True)
    my_print('\nWriting to: ' + out_path_global, show_output=True)

    # Get all file paths that fit 1. given input path, 2. globally defined extensions
    files_ut_paths_unfiltered = get_file_paths(in_path)

    # Get full strings of valid files and their respective paths
    text_strings_full, files_ut_paths = read_text_strings(files_ut_paths_unfiltered)

    # Switch between 'find' best string length and 'use-explicit' string length. No other string allowed
    find_best_str_len_ = input_args[2]

    # Delete citations so they won't pop up in the list of plagiarisms
    text_strings_full = delete_citations_in_texts(text_strings_full)

    # Delete and count each valid bibliography entry
    text_strings_full, num_correct_citations = delete_bibliography(text_strings_full)

    # And output this...
    for files_ut_path, num_correct_citation in zip(files_ut_paths, num_correct_citations):
        my_print(files_ut_path + ' used >>' + str(num_correct_citation) + '<< correct citations. These are excluded from the analysis.', show_output=True)

    # Based on that switch, either find best string length, use given string length or use default string length
    if find_best_str_len_ == '-f' or find_best_str_len_ == '--find':
        best_str_len = find_best_str_len(text_strings_full, files_ut_paths)
    elif find_best_str_len_ == '-e' or find_best_str_len_ == '--use_explicit':
        try:
            best_str_len = int(input_args[3])
        except Exception:
            my_print('No best string length provided. Using default string length.', show_output=True)
            best_str_len = default_best_str_global
    else:
        best_str_len = default_best_str_global
        my_print('False or no argument. Using default string length.', show_output=True)

    # Print used string length and run test
    my_print('\nUsing ' + str(best_str_len) + ' as best string length estimator', show_output=True)
    find_i_subs(text_strings_full, files_ut_paths, False, best_str_len)

    # Write total elapsed time
    time_elapsed_s = time.perf_counter() - start_time
    time_elapsed_m = time_elapsed_s / 60
    my_print('\nTime elapsed: ' + str(round(time_elapsed_s, 2)) + 'sec (' + str(round(time_elapsed_m, 2)) + 'min)', show_output=True)

    # Write out log file
    today = datetime.now()
    iso_date = today.isoformat()
    with open(out_path_global + '/' + str(iso_date).replace('-', '_').replace(':', '_').replace('.', '_') + '___' + os.getlogin() + '.txt', 'a', encoding="utf-8") as log_file:
        log_file.write(string_to_export_global)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Test if any number of documents within the input folder share similar passages of texts')
    parser.add_argument('in', help='Input folder. Each docx, txt, doc and pdf below this directory will be included')
    parser.add_argument('out', help='Path to output folder')
    parser.add_argument('-f', '--find', action='store_true', help='Let the algorithm find the optimal string cutoff length. Might not work perfectly')
    parser.add_argument('-e', '--use_explicit', help='Use a custom string cutoff length. Write 40 if you have absolutely no idea')
    args = parser.parse_args()
    if len(sys.argv) < 2:
        my_print('Please provide useful input. Type \'plariarism_checker -h\' to get help.', show_output=True)
    else:
        main(sys.argv[1:])
