import os
import sys


name = input("Name of the task: ")
time = input("Time when you want the program to check for updates (hour:min <13:15>): ")

exe_loc = sys.executable

bat_W = f"""@echo off
echo Attempting to run the script>>log.txt
cd "{os.getcwd()}"
cd ".."
echo Attempting to run the script>>log.txt

{exe_loc} main.py -m
if %ERRORLEVEL% EQU 0 goto :success

echo All attempts to run the script have failed.
exit /b 1

:success
echo Successfully ran the script.
exit /b 0"""

batch_filename = "auto_W.bat"
with open(batch_filename, 'w') as batch_file:
    batch_file.write(bat_W)

task_name = name
task_run_time = time  # 24-hour format
script_path = os.path.abspath('auto_W.bat')


command = f'Schtasks /Create /SC DAILY /TN "{task_name}" /TR "{script_path}" /ST {task_run_time} /RU SYSTEM /RL HIGHEST'
c = "auto_W.bat"
# Execute the command
os.system(command)