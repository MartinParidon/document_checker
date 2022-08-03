@echo off

set /p doc_path=Enter Link to folder of docs  
set /p best_str_len=Enter best assumed string length  

"venv/Scripts/python.exe" scripts/plagiarism_checker.py %doc_path% check %best_str_len%

pause