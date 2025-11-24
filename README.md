# Prompt Compiler for Cursor

A Python tool that translates Russian queries to English and formats them as prompts for Cursor IDE.

## Features

- 🌐 Automatic translation from Russian to English
- 🎨 Beautiful terminal interface using Rich
- 💬 Interactive mode for continuous use
- 📝 Command-line mode for single translations
- ✨ Formatted output ready for Cursor

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Authentication Setup

The application requires authentication before use. To set up:

1. Create a user database file:

```bash
python setup_auth.py
```


## Usage

### Graphical Interface (GUI)

Launch the graphical interface:

```bash
python gui.py
```

Or use the GUI flag:

```bash
python main.py --gui
```

The GUI provides:
- Input field for Russian text
- Output field for English translation
- Copy to clipboard button
- Clear button
- Keyboard shortcut: Ctrl+Enter to translate

### Interactive Mode (CLI)

Run without arguments to enter interactive mode:

```bash
python main.py
```

Then enter your Russian queries. Type `exit` or `quit` to exit.

### Command-Line Mode

Provide the Russian text as arguments:

```bash
python main.py "Создай функцию для вычисления факториала"
```

## Example

**Input (Russian):**
```
Создай функцию для вычисления факториала числа
```

**Output (English):**
```
Create a function to calculate the factorial of a number
```

## Requirements

- Python 3.7+
- deep-translator
- rich

## License

MIT

