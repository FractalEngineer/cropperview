@echo off
set /p combine=Do you want to combine all videos before processing? (y/n): 
set /p use_gpu=Do you want to use NVIDIA GPU acceleration? (y/n): 
set /p skip_crop=Do you want to skip video cropping? (y/n): 

set cmd_args=

if /i "%combine%"=="y" (
    set cmd_args=%cmd_args% combine
)

if /i "%use_gpu%"=="y" (
    set cmd_args=%cmd_args% gpu
)

if /i "%skip_crop%"=="y" (
    set cmd_args=%cmd_args% nocrop
)

python "cropperview.py" %cmd_args%
pause