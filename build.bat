@echo off
:: ============================================================
:: build.bat  --  Build TowerDefense for distribution (itch.io)
::
:: Requirements:
::   pip install pyinstaller pillow
::
:: Run from the project root:
::   build.bat
::
:: Output:
::   dist\TowerDefense\           -- the game folder
::   dist\TowerDefense.zip        -- ready to upload to itch.io
:: ============================================================

setlocal enabledelayedexpansion

set PROJECT_ROOT=%~dp0
set DIST_DIR=%PROJECT_ROOT%dist
set BUILD_DIR=%PROJECT_ROOT%build
set GAME_DIR=%DIST_DIR%\TowerDefense
set ZIP_FILE=%DIST_DIR%\TowerDefense.zip
set SPEC_FILE=%PROJECT_ROOT%build.spec

echo ============================================================
echo   Mr. Mega's Awesome Tower Defense Game -- itch.io Build
echo ============================================================
echo.

:: ------------------------------------------------------------
:: 0. Verify PyInstaller is available
:: ------------------------------------------------------------
where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller not found.  Run:  pip install pyinstaller
    exit /b 1
)

:: ------------------------------------------------------------
:: 1. Optional: convert icons.png -> icons.ico using Pillow
::    (only runs if Pillow is installed; skipped silently otherwise)
:: ------------------------------------------------------------
echo [1/5] Attempting icon conversion (requires Pillow)...
python -c "from PIL import Image; img=Image.open('assets/images/icons.png'); img.save('assets/images/icons.ico')" 2>nul
if errorlevel 1 (
    echo       Pillow not available or conversion failed -- skipping icon.
) else (
    echo       Icon converted: assets\images\icons.ico
    :: Patch the spec to enable the icon line (replaces the commented-out icon line)
    powershell -Command "(Get-Content '%SPEC_FILE%') -replace '# *icon=''assets/images/icons.ico'',.*', 'icon=''assets/images/icons.ico'',' | Set-Content '%SPEC_FILE%'"
)
echo.

:: ------------------------------------------------------------
:: 2. Clean previous build artifacts
:: ------------------------------------------------------------
echo [2/5] Cleaning previous build output...
if exist "%GAME_DIR%" (
    rmdir /s /q "%GAME_DIR%"
    echo       Removed: %GAME_DIR%
)
if exist "%BUILD_DIR%" (
    rmdir /s /q "%BUILD_DIR%"
    echo       Removed: %BUILD_DIR%
)
if exist "%ZIP_FILE%" (
    del /f /q "%ZIP_FILE%"
    echo       Removed: %ZIP_FILE%
)
echo.

:: ------------------------------------------------------------
:: 3. Run PyInstaller
:: ------------------------------------------------------------
echo [3/5] Running PyInstaller...
pyinstaller "%SPEC_FILE%" --distpath "%DIST_DIR%" --workpath "%BUILD_DIR%" --noconfirm
if errorlevel 1 (
    echo.
    echo [ERROR] PyInstaller failed.  Check the output above for details.
    exit /b 1
)
echo.

:: ------------------------------------------------------------
:: 4. Copy save_data into the dist folder
:: ------------------------------------------------------------
echo [4/5] Copying save_data...
if exist "%PROJECT_ROOT%src\save_data" (
    xcopy /e /i /y "%PROJECT_ROOT%src\save_data" "%GAME_DIR%\src\save_data" >nul
    echo       Copied src\save_data  ->  %GAME_DIR%\src\save_data
) else (
    echo       src\save_data not found -- skipping.
)
echo.

:: ------------------------------------------------------------
:: 5. Create zip archive for itch.io upload
:: ------------------------------------------------------------
echo [5/5] Creating zip archive for itch.io...
powershell -Command "Compress-Archive -Path '%GAME_DIR%\*' -DestinationPath '%ZIP_FILE%' -Force"
if errorlevel 1 (
    echo [ERROR] Failed to create zip archive.
    exit /b 1
)
echo.

:: ------------------------------------------------------------
:: Done
:: ------------------------------------------------------------
echo ============================================================
echo   BUILD SUCCESSFUL
echo ============================================================
echo.
echo   Executable :  %GAME_DIR%\TowerDefense.exe
echo   Upload zip :  %ZIP_FILE%
echo.
echo   To test locally, run:
echo     %GAME_DIR%\TowerDefense.exe
echo.
echo   Upload %ZIP_FILE% to itch.io as a Windows download.
echo ============================================================

endlocal
exit /b 0
