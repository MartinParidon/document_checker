# Text quality estimation tool

## Before you start
* Install Python 3.7 https://www.python.org/downloads/release/python-370/
* Install requirements.txt (Open cmd Window, type: pip install PATH/TO/requirements.txt)

*You should now have a running Python environment with all the necessary libraries*

## Word and phrase checker
*Currently works with docx, txt and PDF. TODO Doc support*
1. Create a custom list of phrases and words. Use the same format as the lists in examples/
2. Customize call_phrase_checker, replacing the paths of the csv files accordingly --> phrases_csv_path=YOUR/LOCAL/PATH.csv (relative or absolute)
3. Double click call_phrase_checker.bat, then specify path to doc under test and output folder
4 Find the output in the specified output folder

## Plagiarism checker
*Currently works with docx, txt and PDF. TODO Doc support*

*This tool will use ALL the documents within any sub folders of the root directory. So if there are 10000 documents anywhere below that folder, it will run through them all.*

*Note that this tool has 2 modes. Try to run it fully automatic by using call_plagiariasm_checker_find.bat. This will find the best string length by itself. If this won't work, you'll need to dig deeper*

### Mode 1: Let the script find the best string length itself
1. Double click call_plagiariasm_find.bat
2. Specify the root folder of your documents under test and your output folder.
4 Find the output in the specified output folder

*The script will attempt to find the best string length. This might not work. If it didn't work or you're not happy with the result, see where the 2 plotted lines in plagiarism_analysis_x_ydiff.png cross for the first time. Use the x value at the cut point to run the script again in the use-explicit mode (see next point)*

### Mode 2: Excplicitly tell the script to use a string length of your choice
*The string length will have direct influence on your results, so be careful!*
1. Double click call_plagiariasm_checker_use_explicit.bat
2. Specify the root folder of your documents under test and your output folder
3. Specify the ideal string length. If you have absolutely no idea, leave it empty. The algorithm will run anyway, with a value of 40.
4 Find the output in the specified output folder

## TODOS
* GUI
* cfg file support (YAML)
* Output formats and structure