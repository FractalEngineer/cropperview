@echo off
set /p combine=Do you want to combine all videos before processing? (y/n): 
set /p use_gpu=Do you want to use NVIDIA GPU acceleration? (y/n): 

if /i "%combine%"=="y" (
    if /i "%use_gpu%"=="y" (
        python "cropperview.py" combine gpu
    ) else (
        python "cropperview.py" combine
    )
) else (
    if /i "%use_gpu%"=="y" (
        python "cropperview.py" gpu
    ) else (
        python "cropperview.py"
    )
)
pause