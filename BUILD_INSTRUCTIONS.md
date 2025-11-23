# Building Executable

## Method 1: Using build.bat (Windows)

1. Double-click `build.bat`
2. Wait for the build to complete
3. Find `PromptCompiler.exe` in the `dist` folder

## Method 2: Manual Build

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Build the executable:
   ```bash
   pyinstaller --onefile --windowed --name=PromptCompiler gui.py --hidden-import=deep_translator --hidden-import=rich --clean --noconfirm
   ```

3. The executable will be in the `dist` folder

## Method 3: Using build_exe.py

```bash
python build_exe.py
```

## Notes

- The executable will be a single file (--onefile)
- No console window will appear (--windowed)
- All dependencies are bundled automatically
- First run might be slightly slower as files are extracted


