@echo off

set /p doc_path=Enter Link to folder of docs  

python scripts/plagiarism_checker.py %doc_path% find

pause