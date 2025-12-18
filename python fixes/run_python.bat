@echo off
REM Crypto Project Python Runner
REM This batch file ensures you always use the correct Python installation

echo ===================================================
echo CRYPTO PROJECT PYTHON RUNNER
echo ===================================================

REM Set the correct Python executable
set PYTHON_EXE=py -3.13

REM Check if numpy is available
echo Checking Python environment...
%PYTHON_EXE% -c "import numpy; import sympy; print('✓ All dependencies available')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Dependencies missing! Running setup...
    %PYTHON_EXE% setup_environment.py
    if %errorlevel% neq 0 (
        echo ❌ Setup failed! Please check your Python installation.
        pause
        exit /b 1
    )
)

REM If no arguments provided, show usage
if "%~1"=="" (
    echo.
    echo USAGE:
    echo   run_python.bat script_name.py
    echo   run_python.bat hill\server.py
    echo   run_python.bat test_hill_imports.py
    echo.
    echo AVAILABLE SCRIPTS:
    echo   - hill\server.py      ^(Hill cipher server^)
    echo   - hill\client.py      ^(Hill cipher client^)
    echo   - ceaser\server.py    ^(Caesar cipher server^)
    echo   - ceaser\client.py    ^(Caesar cipher client^)
    echo   - Vigenere\server.py  ^(Vigenere cipher server^)
    echo   - Vigenere\client.py  ^(Vigenere cipher client^)
    echo   - Vernam\server.py    ^(Vernam cipher server^)
    echo   - Vernam\client.py    ^(Vernam cipher client^)
    echo   - playfair\server.py  ^(Playfair cipher server^)
    echo   - playfair\client.py  ^(Playfair cipher client^)
    echo.
    echo TEST SCRIPTS:
    echo   - test_hill_imports.py
    echo   - test_basic_crypto.py
    echo   - setup_environment.py
    echo.
    pause
    exit /b 0
)

REM Check if file exists
if not exist "%~1" (
    echo ❌ File '%~1' not found!
    echo.
    echo Available Python files:
    for /r %%f in (*.py) do (
        echo   %%~nxf ^(in %%~dpf^)
    )
    echo.
    pause
    exit /b 1
)

REM Run the Python script
echo Running: %~1
echo Command: %PYTHON_EXE% "%~1"
echo ===================================================
%PYTHON_EXE% "%~1" %2 %3 %4 %5 %6 %7 %8 %9

REM Show exit status
if %errorlevel% equ 0 (
    echo.
    echo ✓ Script completed successfully
) else (
    echo.
    echo ❌ Script failed with exit code %errorlevel%
)

echo ===================================================
echo Press any key to close...
pause >nul
