@echo off
echo ====================================
echo  Techware BillSoft v2.0 - Build
echo ====================================
echo.

:: Step 1: Bundle Python backend with PyInstaller
echo [1/3] Bundling Python backend...
cd /d "%~dp0backend"
python -m PyInstaller --clean --noconfirm backend.spec
if errorlevel 1 (
    echo ERROR: PyInstaller failed! Make sure PyInstaller is installed:
    echo   pip install pyinstaller
    exit /b 1
)
echo Backend bundled successfully.
echo.

:: Step 2: Build React frontend
echo [2/3] Building React frontend...
cd /d "%~dp0frontend"
call npm run build
if errorlevel 1 (
    echo ERROR: Frontend build failed!
    exit /b 1
)
echo Frontend built successfully.
echo.

:: Step 3: Package with Electron Builder
echo [3/3] Packaging Electron app...
call npx electron-builder --win
if errorlevel 1 (
    echo ERROR: Electron packaging failed!
    exit /b 1
)
echo.
echo ====================================
echo  BUILD COMPLETE!
echo  Output: release/
echo ====================================
pause
