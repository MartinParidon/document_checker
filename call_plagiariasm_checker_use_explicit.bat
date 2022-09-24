@echo off

set /p doc_path=Enter Link to folder of docs  
set /p out_path=Enter Link to output folder  
set /p best_str_len=Enter best assumed string length  

python scripts/plagiarism_checker.py %doc_path%  %out_path% %best_str_len%

pause