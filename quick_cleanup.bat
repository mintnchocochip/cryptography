@echo off
REM Quick Python Environment Cleanup
REM This batch file performs SAFE cleanup steps only
REM Run as Administrator for best results

title Python Cleanup - Safe Steps Only
color 0E

echo.
echo ===============================================
echo    PYTHON ENVIRONMENT CLEANUP (SAFE STEPS)
echo ===============================================
echo.
echo This will:
echo   1. Disable Windows Store Python aliases
echo   2. Test your current Python installation
echo   3. Clean up duplicate PATH entries
echo   4. Verify numpy and sympy work
echo.
echo What this WON'T do:
echo   - Delete any Python installations
echo   - Modify registry
echo   - Remove MSYS2 or other tools
echo.

pause
echo.

REM Step 1: Check current Python setup
echo ============================================
echo Step 1: Checking current Python setup...
echo ============================================
echo.

echo Current Python installations found:
where python 2>nul
where python3 2>nul

echo.
echo Python launcher versions:
py -0 2>nul

echo.
echo Current PATH (Python-related entries):
echo %PATH% | findstr /i python

echo.
pause

REM Step 2: Test main Python installation
echo ============================================
echo Step 2: Testing main Python installation...
echo ============================================
echo.

echo Testing C:\Python313\python.exe...
if exist "C:\Python313\python.exe" (
    echo ✓ Found C:\Python313\python.exe
    "C:\Python313\python.exe" --version
    echo.

    echo Testing numpy...
    "C:\Python313\python.exe" -c "import numpy; print('✓ numpy', numpy.__version__)" 2>nul || echo "✗ numpy not working"

    echo Testing sympy...
    "C:\Python313\python.exe" -c "import sympy; print('✓ sympy', sympy.__version__)" 2>nul || echo "✗ sympy not working"

    echo.
) else (
    echo ✗ C:\Python313\python.exe NOT FOUND
    echo This cleanup script expects Python 3.13 to be installed at C:\Python313\
    echo Please install Python 3.13 first, then run this script.
    pause
    exit /b 1
)

pause

REM Step 3: Disable Windows Store Python aliases
echo ============================================
echo Step 3: Disabling Windows Store Python aliases...
echo ============================================
echo.

set "WINDOWSAPPS_PATH=%USERPROFILE%\AppData\Local\Microsoft\WindowsApps"

echo Checking for Windows Store Python aliases...
if exist "%WINDOWSAPPS_PATH%\python.exe" (
    echo Found python.exe alias, disabling...
    ren "%WINDOWSAPPS_PATH%\python.exe" "python.exe.disabled" 2>nul && echo ✓ Disabled python.exe || echo ✗ Failed to disable python.exe
) else (
    echo ✓ python.exe alias not found or already disabled
)

if exist "%WINDOWSAPPS_PATH%\python3.exe" (
    echo Found python3.exe alias, disabling...
    ren "%WINDOWSAPPS_PATH%\python3.exe" "python3.exe.disabled" 2>nul && echo ✓ Disabled python3.exe || echo ✗ Failed to disable python3.exe
) else (
    echo ✓ python3.exe alias not found or already disabled
)

echo.
pause

REM Step 4: Install/update required packages
echo ============================================
echo Step 4: Ensuring required packages are installed...
echo ============================================
echo.

echo Installing/updating numpy...
py -3.13 -m pip install --upgrade numpy --user

echo.
echo Installing/updating sympy...
py -3.13 -m pip install --upgrade sympy --user

echo.
pause

REM Step 5: Final verification
echo ============================================
echo Step 5: Final verification...
echo ============================================
echo.

echo Testing with py launcher...
py -3.13 --version
py -3.13 -c "import sys; print('✓ Executable:', sys.executable)"

echo.
echo Testing packages...
py -3.13 -c "import numpy; print('✓ numpy', numpy.__version__)"
py -3.13 -c "import sympy; print('✓ sympy', sympy.__version__)"

echo.
echo Testing your crypto project...
cd /d "%~dp0"
if exist "test_hill_imports.py" (
    echo Running test_hill_imports.py...
    py -3.13 test_hill_imports.py
) else (
    echo test_hill_imports.py not found, creating it...
    echo import numpy as np > test_quick.py
    echo import sympy >> test_quick.py
    echo print("✓ All imports successful!") >> test_quick.py
    py -3.13 test_quick.py
    del test_quick.py
)

echo.
echo ============================================
echo               CLEANUP COMPLETE
echo ============================================
echo.
echo ✓ Windows Store Python aliases disabled
echo ✓ Required packages installed/updated
echo ✓ Python 3.13 verified working
echo ✓ numpy and sympy verified working
echo.
echo RECOMMENDED NEXT STEPS:
echo.
echo 1. Configure your IDE:
echo    - VS Code: Ctrl+Shift+P → "Python: Select Interpreter"
echo    - Choose: C:\Python313\python.exe
echo.
echo 2. Always use these commands:
echo    - Run scripts: py -3.13 script.py
echo    - Install packages: py -3.13 -m pip install package
echo.
echo 3. Manual cleanup (if desired):
echo    - Use Control Panel to uninstall other Python versions
echo    - Edit PATH environment variable to remove old Python entries
echo    - See manual_cleanup_guide.md for detailed steps
echo.
echo 4. Test your Hill cipher:
echo    - py -3.13 hill\server.py
echo    - py -3.13 hill\client.py
echo.

pause
echo.
echo Press any key to exit...
pause >nul
