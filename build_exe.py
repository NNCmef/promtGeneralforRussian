#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import PyInstaller.__main__
import os
import sys

def build_executable():
    print("Building executable...")
    
    PyInstaller.__main__.run([
        'gui.py',
        '--onefile',
        '--windowed',
        '--name=PromptCompiler',
        '--icon=NONE',
        '--add-data=requirements.txt;.',
        '--hidden-import=deep_translator',
        '--hidden-import=rich',
        '--clean',
        '--noconfirm'
    ])
    
    print("\nExecutable built successfully!")
    print("Location: dist/PromptCompiler.exe")

if __name__ == "__main__":
    build_executable()


