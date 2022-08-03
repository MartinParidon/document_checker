Usage

* Install Python 3.7 https://www.python.org/downloads/release/python-370/
* Install requirements.txt (Open cmd Window, type: pip install PATH/TO/requirements.txt)
--> You should now have a running Python environment with all the necessary libraries

Word and phrase checker
--> Currently works with doc, docx and PDF (very old doc files might not work)
1. Create a custom list of phrases and words. Use the same format as the lists in examples/
2. Customize call_phrase_checker, replacing the paths of the csv files accordingly --> phrases_csv_path=YOUR/LOCAL/PATH.csv (relative or absolute)
3. Double click call_phrase_checker.bat, then specify path to doc under test
4. Find output in out/

Plagiarism checker
--> Currently works with doc, docx and PDF, as well as txt (very old doc files might not work)
--> This tool will use ALL the documents within any sub folders of the root directory. So if there are 10000 documents anywhere below that folder, it will run through them all.
--> Not that this tool has 2 modes. First mode (pre-check) is to analyse the structure of your texts. In short, it will tell you which parameter to specify for the actual check.
****** Pre-Check
1. Double click call_plagiariasm_pre_check.bat
2. Specify the root folder of your documents under test
3. Find output in out/
4. From this output, read the "best" string length cutoff value. That is the x value where your chart stays more or less flat. This value will be used in the actual analysis and results will be depending on this value directly.
****** Checker
1. Double click call_plagiariasm_checker.bat
2. Specify the root folder of your documents under test
3. Specify the number that you found using the pre-checker. If you have absolutely no idea, write 50.
4. Find output in out/

TODOS
* Input sanity checks and early out (?)
* GUI
* cfg file support (YAML)
* Percentages and diagrams