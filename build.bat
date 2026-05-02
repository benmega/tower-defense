@echo off
echo Building Tower Defense for itch.io...

echo Installing build dependencies...
pip install pyinstaller pillow

echo Running PyInstaller...
pyinstaller build.spec

if %errorlevel% neq 0 (
    echo Build failed!
    exit /b 1
)

echo Creating distribution zip...
cd dist
powershell -Command "Compress-Archive -Path 'TowerDefense' -DestinationPath 'TowerDefense.zip' -Force"
cd ..

if exist dist\TowerDefense.zip (
    echo.
    echo Build successful!
    echo Distribution ready at: dist\TowerDefense.zip
) else (
    echo.
    echo Failed to create distribution zip
    exit /b 1
)
