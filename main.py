#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Optional
from deep_translator import GoogleTranslator  # pyright: ignore[reportMissingImports]
from rich.console import Console  # pyright: ignore[reportMissingImports]
from rich.panel import Panel  # pyright: ignore[reportMissingImports]
from rich.text import Text  # pyright: ignore[reportMissingImports]
from rich.prompt import Prompt  # pyright: ignore[reportMissingImports]


class PromptCompiler:
    
    def __init__(self):
        self.console = Console()
        self.translator = GoogleTranslator(source='ru', target='en')
    
    def translate(self, russian_text: str) -> str:
        try:
            english_text = self.translator.translate(russian_text)
            return english_text
        except Exception as e:
            self.console.print(f"[red]Translation error: {e}[/red]")
            return russian_text
    
    def format_prompt(self, original: str, translated: str) -> str:
        formatted = f"""Original (Russian): {original}

Translated (English): {translated}

---
Formatted Prompt for Cursor:
{translated}"""
        return formatted
    
    def display_result(self, original: str, translated: str):
        result_text = Text()
        result_text.append("Original Query (Russian):\n", style="bold cyan")
        result_text.append(f"{original}\n\n", style="white")
        result_text.append("Translated Query (English):\n", style="bold green")
        result_text.append(f"{translated}\n\n", style="white")
        result_text.append("─" * 60 + "\n", style="dim")
        result_text.append("Ready to use in Cursor:\n", style="bold yellow")
        result_text.append(f"{translated}", style="bright_white")
        
        panel = Panel(
            result_text,
            title="[bold magenta]Prompt Compiler for Cursor[/bold magenta]",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")
    
    def run_interactive(self):
        self.console.print("[bold magenta]Prompt Compiler for Cursor[/bold magenta]")
        self.console.print("[dim]Enter your query in Russian. Type 'exit' or 'quit' to exit.[/dim]\n")
        
        while True:
            try:
                russian_query = Prompt.ask("[cyan]Enter Russian query[/cyan]")
                
                if russian_query.lower() in ['exit', 'quit', 'выход']:
                    self.console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if not russian_query.strip():
                    continue
                
                self.console.print("[dim]Translating...[/dim]")
                english_query = self.translate(russian_query)
                self.display_result(russian_query, english_query)
                
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]Error: {e}[/red]")
    
    def run_single(self, russian_text: str):
        english_text = self.translate(russian_text)
        self.display_result(russian_text, english_text)
        return english_text


def main():
    # Check for GUI mode
    if len(sys.argv) > 1 and sys.argv[1] in ['--gui', '-g', 'gui']:
        try:
            from gui import main as gui_main
            gui_main()
        except ImportError as e:
            print(f"GUI mode requires tkinter. Error: {e}")
            print("Falling back to CLI mode...")
            compiler = PromptCompiler()
            compiler.run_interactive()
        return
    
    compiler = PromptCompiler()
    
    if len(sys.argv) > 1:
        # Command line mode: translate the provided text
        russian_text = " ".join(sys.argv[1:])
        compiler.run_single(russian_text)
    else:
        # Interactive mode
        compiler.run_interactive()


if __name__ == "__main__":
    main()

