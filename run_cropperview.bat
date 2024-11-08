@echo off
set /p combine=Do you want to combine all videos before processing? (y/n): 
if /i "%combine%"=="y" (
    python "cropperview.py" combine
) else (
    python "cropperview.py"
)
pause