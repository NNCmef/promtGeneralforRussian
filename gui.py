#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from deep_translator import GoogleTranslator  # pyright: ignore[reportMissingImports]


class PromptCompilerGUI:
    # Midnight theme colors
    BG_DARK = "#0d1117"  # Deep dark blue-black
    BG_SECONDARY = "#161b22"  # Slightly lighter dark
    BG_TERTIARY = "#21262d"  # Even lighter for frames
    TEXT_PRIMARY = "#c9d1d9"  # Light gray text
    TEXT_SECONDARY = "#8b949e"  # Muted gray
    ACCENT_CYAN = "#58a6ff"  # Bright cyan blue
    ACCENT_PURPLE = "#bc8cff"  # Purple accent
    BORDER_COLOR = "#30363d"  # Subtle border
    INPUT_BG = "#0d1117"  # Dark input background
    BUTTON_BG = "#21262d"  # Button background
    BUTTON_HOVER = "#30363d"  # Button hover
    SUCCESS_GREEN = "#3fb950"  # Success green
    ERROR_RED = "#f85149"  # Error red
    
    def __init__(self, root):
        self.root = root
        self.root.title("Prompt Compiler for Cursor")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        self.pinned = False
        
        # Configure midnight theme
        self.setup_theme()
        
        # Initialize translator
        self.translator = GoogleTranslator(source='ru', target='en')
        
        # Setup UI
        self.setup_ui()
        
        # Center window
        self.center_window()
    
    def setup_theme(self):
        self.root.configure(bg=self.BG_DARK)
        
        # Configure ttk style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Frame styles
        self.style.configure('Dark.TFrame', background=self.BG_DARK)
        self.style.configure('Secondary.TFrame', background=self.BG_SECONDARY)
        
        # LabelFrame styles
        self.style.configure(
            'Dark.TLabelframe',
            background=self.BG_DARK,
            foreground=self.TEXT_PRIMARY,
            bordercolor=self.BORDER_COLOR,
            relief=tk.FLAT
        )
        self.style.configure(
            'Dark.TLabelframe.Label',
            background=self.BG_DARK,
            foreground=self.ACCENT_CYAN,
            font=("Segoe UI", 10, "bold")
        )
        
        # Label styles
        self.style.configure(
            'Dark.TLabel',
            background=self.BG_DARK,
            foreground=self.TEXT_PRIMARY,
            font=("Segoe UI", 9)
        )
        self.style.configure(
            'Title.TLabel',
            background=self.BG_DARK,
            foreground=self.ACCENT_CYAN,
            font=("Segoe UI", 20, "bold")
        )
        self.style.configure(
            'Status.TLabel',
            background=self.BG_DARK,
            foreground=self.TEXT_SECONDARY,
            font=("Segoe UI", 9)
        )
        
        # Button styles
        self.style.configure(
            'Accent.TButton',
            background=self.ACCENT_CYAN,
            foreground="#ffffff",
            borderwidth=0,
            focuscolor='none',
            font=("Segoe UI", 10, "bold"),
            padding=10
        )
        self.style.map(
            'Accent.TButton',
            background=[('active', '#6ab8ff'), ('pressed', '#4a96ff')]
        )
        
        self.style.configure(
            'Dark.TButton',
            background=self.BUTTON_BG,
            foreground=self.TEXT_PRIMARY,
            borderwidth=0,
            focuscolor='none',
            font=("Segoe UI", 10),
            padding=8
        )
        self.style.map(
            'Dark.TButton',
            background=[('active', self.BUTTON_HOVER), ('pressed', self.BG_TERTIARY)]
        )
    
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="25")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        title_frame.grid(row=0, column=0, pady=(0, 25), sticky=(tk.W, tk.E))
        
        title_label = ttk.Label(
            title_frame,
            text="✨ Prompt Compiler for Cursor",
            style="Title.TLabel"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Translate Russian queries to English prompts",
            style="Status.TLabel"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Input section
        input_frame = ttk.LabelFrame(
            main_frame,
            text="📝 Russian Query (Введите запрос на русском)",
            style='Dark.TLabelframe',
            padding="15"
        )
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        text_frame = tk.Frame(input_frame, bg=self.BG_TERTIARY, relief=tk.FLAT, bd=1)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        self.input_text = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            width=70,
            height=8,
            font=("Segoe UI", 11),
            bg=self.INPUT_BG,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_CYAN,
            selectbackground=self.ACCENT_CYAN,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=12,
            highlightthickness=0
        )
        self.input_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.input_text.focus()
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        buttons_frame.grid(row=2, column=0, pady=15)
        
        # Translate button
        self.translate_button = ttk.Button(
            buttons_frame,
            text="🚀 Translate (Перевести)",
            command=self.translate_text,
            style="Accent.TButton"
        )
        self.translate_button.pack(side=tk.LEFT, padx=8)
        
        # Clear button
        clear_button = ttk.Button(
            buttons_frame,
            text="🗑️ Clear (Очистить)",
            command=self.clear_all,
            style="Dark.TButton"
        )
        clear_button.pack(side=tk.LEFT, padx=8)
        
        # Pin/Unpin button
        self.pin_button = ttk.Button(
            buttons_frame,
            text="📌 Pin Window",
            command=self.toggle_pin,
            style="Dark.TButton"
        )
        self.pin_button.pack(side=tk.LEFT, padx=8)
        
        # Output section
        output_frame = ttk.LabelFrame(
            main_frame,
            text="🌐 English Translation (Английский перевод)",
            style='Dark.TLabelframe',
            padding="15"
        )
        output_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        # Text output widget
        output_text_frame = tk.Frame(output_frame, bg=self.BG_TERTIARY, relief=tk.FLAT, bd=1)
        output_text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        output_text_frame.columnconfigure(0, weight=1)
        output_text_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(
            output_text_frame,
            wrap=tk.WORD,
            width=70,
            height=8,
            font=("Segoe UI", 11),
            bg=self.INPUT_BG,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_CYAN,
            selectbackground=self.ACCENT_CYAN,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            padx=12,
            pady=12,
            highlightthickness=0,
            state=tk.DISABLED
        )
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Copy button frame
        copy_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        copy_frame.grid(row=4, column=0, pady=10)
        
        # Copy to clipboard button
        copy_button = ttk.Button(
            copy_frame,
            text="📋 Copy to Clipboard (Копировать в буфер)",
            command=self.copy_to_clipboard,
            style="Dark.TButton"
        )
        copy_button.pack(side=tk.LEFT, padx=8)
        
        # Status label with icon
        status_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        status_frame.grid(row=5, column=0, pady=10)
        
        self.status_label = ttk.Label(
            status_frame,
            text="● Ready",
            style="Status.TLabel"
        )
        self.status_label.pack()
        
        # Bind Enter key (Ctrl+Enter for multiline)
        self.input_text.bind('<Control-Return>', lambda e: self.translate_text())
        self.root.bind('<Control-Return>', lambda e: self.translate_text())
        
        # Configure scrollbar colors
        self._style_scrollbars()
    
    def _style_scrollbars(self):
        try:
            self.root.option_add('*TScrollbar*background', self.BG_TERTIARY)
            self.root.option_add('*TScrollbar*troughcolor', self.BG_DARK)
            self.root.option_add('*TScrollbar*borderwidth', 0)
            self.root.option_add('*TScrollbar*arrowcolor', self.TEXT_SECONDARY)
            self.root.option_add('*TScrollbar*activebackground', self.BUTTON_HOVER)
        except:
            pass  # Scrollbar styling may not work on all systems
    
    def translate_text(self):
        russian_text = self.input_text.get("1.0", tk.END).strip()
        
        if not russian_text:
            messagebox.showwarning("Warning", "Please enter text to translate")
            return
        
        # Disable button and show status
        self.translate_button.config(state=tk.DISABLED)
        self.status_label.config(text="⏳ Translating...", foreground=self.ACCENT_CYAN)
        self.root.update()
        
        # Run translation in background thread
        thread = threading.Thread(target=self._translate_thread, args=(russian_text,))
        thread.daemon = True
        thread.start()
    
    def _translate_thread(self, russian_text: str):
        try:
            english_text = self.translator.translate(russian_text)
            
            # Update UI
            self.root.after(0, self._update_output, english_text, None)
        except Exception as e:
            error_msg = f"Translation error: {str(e)}"
            self.root.after(0, self._update_output, None, error_msg)
    
    def _update_output(self, english_text: str = None, error: str = None):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        
        if error:
            self.output_text.insert("1.0", error)
            self.output_text.tag_add("error", "1.0", tk.END)
            self.output_text.tag_config("error", foreground=self.ERROR_RED)
            self.status_label.config(text="❌ Error occurred", foreground=self.ERROR_RED)
        else:
            self.output_text.insert("1.0", english_text)
            self.status_label.config(text="✅ Translation complete", foreground=self.SUCCESS_GREEN)
        
        self.output_text.config(state=tk.DISABLED)
        self.translate_button.config(state=tk.NORMAL)
    
    def copy_to_clipboard(self):
        english_text = self.output_text.get("1.0", tk.END).strip()
        
        if not english_text:
            messagebox.showwarning("Warning", "No text to copy")
            return
        
        self.root.clipboard_clear()
        self.root.clipboard_append(english_text)
        self.status_label.config(text="✅ Copied to clipboard!", foreground=self.SUCCESS_GREEN)
        
        # Reset status after 2 seconds
        self.root.after(2000, lambda: self.status_label.config(text="● Ready", foreground=self.TEXT_SECONDARY))
    
    def clear_all(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_label.config(text="🗑️ Cleared", foreground=self.TEXT_SECONDARY)
        self.input_text.focus()
        
        # Reset status after 1 second
        self.root.after(1000, lambda: self.status_label.config(text="● Ready", foreground=self.TEXT_SECONDARY))
    
    def toggle_pin(self):
        """Toggle window always on top"""
        self.pinned = not self.pinned
        self.root.attributes('-topmost', self.pinned)
        if self.pinned:
            self.pin_button.config(text="📌 Unpin Window")
            self.status_label.config(text="📌 Window pinned", foreground=self.ACCENT_CYAN)
        else:
            self.pin_button.config(text="📌 Pin Window")
            self.status_label.config(text="● Window unpinned", foreground=self.TEXT_SECONDARY)
        
        # Reset status after 2 seconds
        self.root.after(2000, lambda: self.status_label.config(text="● Ready", foreground=self.TEXT_SECONDARY))
    
    def toggle_pin(self):
        """Toggle window always on top"""
        self.pinned = not self.pinned
        self.root.attributes('-topmost', self.pinned)
        if self.pinned:
            self.pin_button.config(text="📌 Unpin Window")
            self.status_label.config(text="📌 Window pinned", foreground=self.ACCENT_CYAN)
        else:
            self.pin_button.config(text="📌 Pin Window")
            self.status_label.config(text="● Window unpinned", foreground=self.TEXT_SECONDARY)
        
        # Reset status after 2 seconds
        self.root.after(2000, lambda: self.status_label.config(text="● Ready", foreground=self.TEXT_SECONDARY))


def main():
    root = tk.Tk()
    app = PromptCompilerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

