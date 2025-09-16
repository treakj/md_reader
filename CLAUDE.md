# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**MD Reader** is a Python-based desktop Markdown viewer with PDF export functionality for Windows. It's designed as a simple, elegant alternative to complex Markdown editors, focusing specifically on viewing and converting Markdown documents.

## Key Development Commands

### Running the Application
- **Development mode** (with console for debugging): `python markdown_reader.py`
- **Production mode** (no console): `python leitor_md.pyw`
- **Windows default program** (recommended for file association): `md_reader.bat`

### Dependency Management
- Install dependencies: `pip install -r requirements.txt`
- Upgrade dependencies: `pip install --upgrade -r requirements.txt`

## Architecture and Structure

### Main Entry Points
- `markdown_reader.py` - Core application logic (440 lines, main `MarkdownReader` class)
- `leitor_md.pyw` - Production launcher (imports and runs main app, no console)
- `md_reader.bat` - Windows batch launcher for reliable file association

### Key Dependencies and Fallbacks
The application uses a fallback architecture:
- **PDF Generation**: WeasyPrint (preferred) → ReportLab (fallback)
- **HTML Rendering**: tkinterweb (preferred) → plain Tkinter text widget (fallback)
- **Markdown Processing**: Python-Markdown with extensions
- **Syntax Highlighting**: Pygments

### Important Technical Details

#### Dual-Mode Execution
- `.py` files show console (for development/debug)
- `.pyw` files hide console (for production/normal use)
- The `.bat` file is specifically for Windows default program registration

#### Windows-Specific Considerations
- GTK3 runtime required for WeasyPrint (optional)
- Batch file handles proper directory navigation and error messages
- Supports multiple Markdown extensions: `.md`, `.markdown`, `.mdown`, `.mkd`, `.mkdn`

#### Error Handling
- Graceful fallbacks for missing optional dependencies
- User-friendly error messages in Portuguese
- Comprehensive exception handling throughout the codebase

### File Structure
```
├── markdown_reader.py      # Main application (MarkdownReader class)
├── leitor_md.pyw           # Production launcher (no console)
├── md_reader.bat           # Windows default program launcher
├── requirements.txt        # Pinned dependencies
├── sample.md              # Test file
└── Documentation files    # README.md, INSTALL.md, WINDOWS_SETUP.md
```

## Development Notes

### Working with the Code
- The main logic is in `markdown_reader.py:43` (MarkdownReader class)
- The application uses Tkinter for GUI with optional HTML rendering via tkinterweb
- PDF export has two paths: WeasyPrint (CSS-based) or ReportLab (programmatic)
- All dependencies are pinned in requirements.txt for reproducible builds

### Testing and Debugging
- Use `markdown_reader.py` for development (visible console for debugging)
- Use `leitor_md.pyw` for testing production behavior
- Test file association scenarios with `md_reader.bat`

### Windows Integration
- The batch file is designed for reliable Windows default program association
- It handles directory navigation and provides Portuguese error messages
- Always test default program functionality with the `.bat` file