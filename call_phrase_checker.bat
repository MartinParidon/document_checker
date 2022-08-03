@echo off

set phrases_csv_path=examples/phrases_examples.csv
set words_csv_path=examples/words_examples.csv

set /p doc_path=Enter Link to Document  

python scripts/phrase_checker.py %doc_path% %phrases_csv_path% %words_csv_path%

pause