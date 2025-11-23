@echo off
echo Installing PyInstaller...
pip install pyinstaller

echo.
echo Building executable...
pyinstaller --onefile --windowed --name=PromptCompiler gui.py --hidden-import=deep_translator --hidden-import=rich --clean --noconfirm

echo.
echo Build complete! Check the dist folder for PromptCompiler.exe
pause


