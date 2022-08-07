import glob
import docx2txt
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import time
from datetime import datetime
from pyvis.network import Network
import os
import sys


# TODO consolidate
types_global = ['/**/*.pdf', '/**/*.doc', '/**/*.docx', '/**/*.txt']

debug_on_global = False

# Search n_optimal
best_len_str_search_d_chars_global = 2
best_len_str_search_min_range_global = 10
best_len_str_search_max_range_global = 60

test_ON = False

string_to_export_global = ''

in_path_global = ''
out_path_global = ''

default_best_str_global = 40

default_cutoff_global = 0.9


def get_file_paths(root_dir):
    types = []
    for type_iter in types_global:
        types.append(root_dir + type_iter)
    files_grabbed = []
    for files in types:
        files_grabbed.extend(glob.glob(files, recursive=True))
    file_paths = []
    [file_paths.append(file.replace('\\', '/')) for file in files_grabbed if (file.split('.')[-1] == 'pdf' or file.split('.')[-1] == 'doc' or file.split('.')[-1] == 'docx' or file.split('.')[-1] == 'txt')]
    my_print(file_paths)
    return file_paths


# TODO consolidate with phrase_checker
def get_full_text(text_path):
    # TODO check with types_global
    txt_file_ext = text_path.split('.')[-1]
    if (txt_file_ext == 'doc') or (txt_file_ext == 'docx'):
        try:
            full_text_ut = docx2txt.process(text_path)
            if full_text_ut:
                return full_text_ut
            else:
                return None
        except Exception:
            return None
    elif txt_file_ext == 'pdf':
        reader = PdfReader(text_path)
        full_text_ut = ""
        for page in reader.pages:
            try:
                full_text_ut += page.extract_text() + " "
            except Exception:
                continue
        if full_text_ut:
            return full_text_ut
        else:
            return None
    elif txt_file_ext == 'txt':
        with open(text_path, "r") as text_file:
            full_text_ut = text_file.read()
            if full_text_ut:
                return full_text_ut
            else:
                return None


def read_text_strings(files_ut_paths):
    full_text_ut_list = []
    files_ut_paths_to_remove = []
    for i_path, text_path in enumerate(files_ut_paths):
        my_print('\n\n')
        full_text_raw = get_full_text(text_path)
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


def set_and_make_out_dir(in_path):
    global out_path_global
    global in_path_global
    if not len(os.listdir(in_path)) == 0:
        in_path_global = in_path
        out_path_global = os.path.split(os.path.realpath(__file__))[0] + '/../out/' + in_path_global.replace('\\', '_').replace(':', '_')
        os.makedirs(out_path_global, exist_ok=True)
    else:
        quit()


def main(argv):
    start_time = round(time.perf_counter(), 2)

    global out_path_global
    global default_best_str_global
    global string_to_export_global

    string_to_export_global = ''

    find_best_str_len_ = argv[1]

    set_and_make_out_dir(argv[0])

    my_print('\nTesting: ' + argv[0], show_output=True)

    files_ut_paths_unfiltered = get_file_paths(argv[0])

    text_strings_full, files_ut_paths = read_text_strings(files_ut_paths_unfiltered)

    if find_best_str_len_ == 'find':
        best_str_len = find_best_str_len(text_strings_full, files_ut_paths)
    elif find_best_str_len_ == 'use-explicit':
        try:
            best_str_len = int(argv[2])
        except Exception:
            my_print('No best string length provided. Using default string length.', show_output=True)
            best_str_len = default_best_str_global
    else:
        best_str_len = default_best_str_global
        my_print('False or no argument. Using default string length.', show_output=True)

    my_print('Using ' + str(best_str_len) + ' as best string length estimator', show_output=True)
    find_i_subs(text_strings_full, files_ut_paths, False, best_str_len)

    time_elapsed_s = time.perf_counter() - start_time
    time_elapsed_m = time_elapsed_s / 60
    my_print('\nTime elapsed: ' + str(round(time_elapsed_s, 2)) + 'sec (' + str(round(time_elapsed_m, 2)) + 'min)', show_output=True)

    today = datetime.now()
    iso_date = today.isoformat()
    with open(out_path_global + '/' + str(iso_date).replace('-', '_').replace(':', '_').replace('.', '_') + '___' + os.getlogin() + '.txt', 'a', encoding="utf-8") as log_file:
        log_file.write(string_to_export_global)

    pass


if __name__ == "__main__":
    if test_ON:
        #main([r'D:\anderes\Textdokumente\Schulreferate', 'find'])
        #main([r'D:\anderes\Textdokumente\Geschreibsel', 'find'])
        #main([r'D:\Geschäftlich\Bewerbungsunterlagen\Lebenslauf', 'find'])
        #main([r'D:\Geschäftlich\Bewerbungsunterlagen\Bewerbungen', 'find'])
        #main([r'D:\anderes\Textdokumente\Schulreferate', 'use-explicit'])
        #main([r'D:\anderes\Textdokumente\Geschreibsel', 'use-explicit', '20'])
        #main([r'D:\Geschäftlich\Bewerbungsunterlagen\Lebenslauf', 'use-explicit', '50'])
        #main([r'D:\Geschäftlich\Bewerbungsunterlagen\Bewerbungen', 'use-explicit', '60'])
        pass
    else:
        main(sys.argv[1:])
