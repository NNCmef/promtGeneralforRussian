#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import hashlib
import json
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, messagebox
import threading


class AuthWindow:
    BG_DARK = "#0d1117"
    BG_SECONDARY = "#161b22"
    BG_TERTIARY = "#21262d"
    TEXT_PRIMARY = "#c9d1d9"
    TEXT_SECONDARY = "#8b949e"
    ACCENT_CYAN = "#58a6ff"
    SUCCESS_GREEN = "#3fb950"
    ERROR_RED = "#f85149"
    BORDER_COLOR = "#30363d"
    BUTTON_BG = "#21262d"
    BUTTON_HOVER = "#30363d"
    INPUT_BG = "#161b22"
    
    GITHUB_DB_URL = "https://raw.githubusercontent.com/NNCmef/GITHUB_DB_URL/main/users.json"
    
    def __init__(self, root, on_success_callback):
        self.root = root
        self.root.title("Authentication")
        self.root.geometry("450x350")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.focus_force()
        self.on_success = on_success_callback
        self.authenticated = False
        self.user_db = {}
        self.attempts = 0
        self.max_attempts = 5
        
        self.setup_theme()
        self.setup_ui()
        self.center_window()
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(lambda: self.root.attributes('-topmost', False))
    
    def _on_close(self):
        self.root.quit()
        self.root.destroy()
    
    def setup_theme(self):
        self.root.configure(bg=self.BG_DARK)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Dark.TFrame', background=self.BG_DARK)
        self.style.configure(
            'Dark.TLabel',
            background=self.BG_DARK,
            foreground=self.TEXT_PRIMARY,
            font=("Segoe UI", 10)
        )
        self.style.configure(
            'Title.TLabel',
            background=self.BG_DARK,
            foreground=self.ACCENT_CYAN,
            font=("Segoe UI", 18, "bold")
        )
        self.style.configure(
            'Status.TLabel',
            background=self.BG_DARK,
            foreground=self.TEXT_SECONDARY,
            font=("Segoe UI", 9)
        )
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
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(
            main_frame,
            text="🔐 Authentication",
            style="Title.TLabel"
        )
        title_label.pack(pady=(0, 30))
        
        login_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        login_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            login_frame,
            text="Username:",
            style="Dark.TLabel"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        username_frame = tk.Frame(login_frame, bg=self.BG_TERTIARY, relief=tk.FLAT, bd=2, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        username_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=("Segoe UI", 11),
            bg=self.INPUT_BG,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_CYAN,
            selectbackground=self.ACCENT_CYAN,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=12,
            exportselection=0
        )
        self.username_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.username_entry.config(state=tk.NORMAL)
        self.root.after(200, lambda: [self.username_entry.focus_set(), self.username_entry.icursor(0)])
        
        ttk.Label(
            login_frame,
            text="Password:",
            style="Dark.TLabel"
        ).pack(anchor=tk.W, pady=(0, 5))
        
        password_frame = tk.Frame(login_frame, bg=self.BG_TERTIARY, relief=tk.FLAT, bd=2, highlightbackground=self.BORDER_COLOR, highlightthickness=1)
        password_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Segoe UI", 11),
            bg=self.INPUT_BG,
            fg=self.TEXT_PRIMARY,
            insertbackground=self.ACCENT_CYAN,
            selectbackground=self.ACCENT_CYAN,
            selectforeground="#ffffff",
            relief=tk.FLAT,
            borderwidth=0,
            highlightthickness=0,
            padx=12,
            pady=12,
            show="*",
            exportselection=0
        )
        self.password_entry.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.password_entry.config(state=tk.NORMAL)
        self.password_entry.bind('<Return>', lambda e: self.authenticate())
        
        button_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        button_frame.pack(fill=tk.X, pady=10)
        
        self.login_button = ttk.Button(
            button_frame,
            text="🚀 Login",
            command=self.authenticate,
            style="Accent.TButton"
        )
        self.login_button.pack(fill=tk.X)
        
        self.status_label = ttk.Label(
            main_frame,
            text="",
            style="Status.TLabel"
        )
        self.status_label.pack(pady=(15, 0))
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def fetch_user_db(self):
        try:
            req = urllib.request.Request(
                self.GITHUB_DB_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                if response.getcode() != 200:
                    return None
                data = response.read().decode('utf-8')
                if len(data) > 100000:
                    return None
                parsed = json.loads(data)
                if not isinstance(parsed, dict):
                    return None
                return parsed
        except urllib.error.URLError:
            return None
        except json.JSONDecodeError:
            return None
        except Exception:
            return None
    
    def authenticate(self):
        if self.attempts >= self.max_attempts:
            self.status_label.config(
                text="❌ Too many failed attempts. Please restart the application.",
                foreground=self.ERROR_RED
            )
            self.login_button.config(state=tk.DISABLED)
            self.username_entry.config(state=tk.DISABLED)
            self.password_entry.config(state=tk.DISABLED)
            return
        
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            self.status_label.config(
                text="❌ Please enter both username and password",
                foreground=self.ERROR_RED
            )
            return
        
        if len(username) > 50 or len(password) > 100:
            self.status_label.config(
                text="❌ Invalid input length",
                foreground=self.ERROR_RED
            )
            return
        
        self.login_button.config(state=tk.DISABLED)
        self.status_label.config(
            text="⏳ Authenticating...",
            foreground=self.ACCENT_CYAN
        )
        self.root.update()
        
        thread = threading.Thread(target=self._auth_thread, args=(username, password))
        thread.daemon = True
        thread.start()
    
    def _auth_thread(self, username, password):
        user_db = self.fetch_user_db()
        
        if user_db is None:
            self.root.after(0, self._auth_failed, "Failed to connect to authentication server")
            return
        
        password_hash = self.hash_password(password)
        
        if username in user_db and user_db[username] == password_hash:
            self.authenticated = True
            self.root.after(0, self._auth_success)
        else:
            self.root.after(0, self._auth_failed, "Invalid username or password")
    
    def _auth_success(self):
        self.status_label.config(
            text="✅ Authentication successful",
            foreground=self.SUCCESS_GREEN
        )
        self.root.after(500, self._close_and_continue)
    
    def _auth_failed(self, message):
        self.attempts += 1
        remaining = self.max_attempts - self.attempts
        if remaining > 0:
            msg = f"❌ {message} ({remaining} attempts remaining)"
        else:
            msg = f"❌ {message}. Maximum attempts reached."
        self.status_label.config(
            text=msg,
            foreground=self.ERROR_RED
        )
        if self.attempts < self.max_attempts:
            self.login_button.config(state=tk.NORMAL)
        self.password_entry.delete(0, tk.END)
    
    def _close_and_continue(self):
        callback = self.on_success
        self.root.withdraw()
        self.root.update()
        self.root.after(50, lambda: [self.root.destroy(), callback() if callback else None])

