@echo off

set /p doc_path=Enter Link to folder of docs  
set /p out_path=Enter Link to output folder  

python scripts/plagiarism_checker.py %doc_path%  %out_path% find

pause