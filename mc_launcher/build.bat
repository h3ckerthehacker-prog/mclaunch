@echo off
echo ============================================
echo   MC Launcher - Build Script
echo   Requires: Python 3, pip
echo ============================================
echo.

:: Install dependencies
echo [1/3] Installing PyInstaller...
pip install pyinstaller --quiet
if errorlevel 1 (
    echo ERROR: pip install failed. Make sure Python is installed.
    pause
    exit /b 1
)

:: Copy the mod next to the script (PyInstaller will bundle it)
echo [2/3] Preparing files...
copy /Y "gradle-wrapper.jar" "gradle-wrapper.jar" >nul 2>&1

:: Build the .exe
echo [3/3] Building launcher.exe ...
pyinstaller ^
    --onefile ^
    --windowed ^
    --name "MC-Launcher-1.12.2" ^
    --add-data "gradle-wrapper.jar;." ^
    --icon NONE ^
    launcher.py

echo.
echo ============================================
if exist "dist\MC-Launcher-1.12.2.exe" (
    echo   SUCCESS! Your .exe is in the dist\ folder.
    echo   dist\MC-Launcher-1.12.2.exe
) else (
    echo   Build may have failed - check output above.
)
echo ============================================
pause
