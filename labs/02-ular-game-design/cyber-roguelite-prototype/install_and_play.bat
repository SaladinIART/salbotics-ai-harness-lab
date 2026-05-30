@echo off
setlocal

cd /d "%~dp0"

echo.
echo Ular Cyber-Roguelite Prototype
echo Installing local environment...
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON_CMD=python"
    ) else (
        echo ERROR: Python was not found. Install Python 3.10+ and try again.
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 goto failed
) else (
    echo Existing virtual environment found.
)

echo Upgrading pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto failed

echo Installing prototype package...
".venv\Scripts\python.exe" -m pip install -e .
if errorlevel 1 goto failed

echo Running tests...
".venv\Scripts\python.exe" -m unittest discover -s tests
if errorlevel 1 goto failed

echo.
echo Installation complete. Starting game...
echo.
".venv\Scripts\python.exe" -m ular_cyber_roguelite
if errorlevel 1 goto failed

echo.
echo Game closed.
pause
exit /b 0

:failed
echo.
echo ERROR: Installation or launch failed. Check the message above.
pause
exit /b 1

