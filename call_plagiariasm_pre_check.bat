@echo off

set /p doc_path=Enter Link to folder of docs  

"venv/Scripts/python.exe" scripts/plagiarism_checker.py %doc_path% pre_check

pause