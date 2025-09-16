# Changelog

All notable changes to this project will be documented in this file.

## [v2.0.1] - 2025-01-16

### 🐛 Bug Fixes

- **Fixed CSS f-string escaping issues**: Corrected missing double braces `{{}}` in CSS blocks that were causing `NameError` when opening markdown files
  - Fixed `h1, h2, h3, h4, h5, h6` CSS block escaping
  - Fixed `pre code` CSS block escaping  
  - Fixed `img` CSS block escaping
  - Fixed `a:hover` CSS block escaping

- **Fixed HtmlFrame background configuration**: Removed invalid `bg` parameter configuration that was causing `TclError: unknown option "-bg"` errors

- **Fixed dark mode functionality**: Dark mode now properly applies to both UI elements and document content
  - Document background changes from white to dark gray
  - Text colors switch from black to white
  - Code blocks, tables, and links get appropriate dark theme colors
  - Theme changes are applied dynamically when toggling

- **Fixed zoom functionality**: Zoom controls now properly scale document content
  - Dynamic font size calculation based on zoom level (50% - 300%)
  - Font sizes update in real-time when using zoom buttons or keyboard shortcuts
  - Zoom level persists in configuration

### ✨ Improvements

- **Enhanced CSS generation**: Added dynamic theme and zoom-based styling
  - Colors automatically adjust based on dark/light mode
  - Font sizes scale proportionally with zoom level
  - Improved contrast and readability in dark mode

- **Better error handling**: Improved error messages and logging for CSS generation issues

### 🔧 Technical Changes

- Refactored `create_html_document()` method to use proper f-string escaping
- Updated dark/light mode methods to refresh HTML content dynamically
- Enhanced zoom update logic to trigger content refresh for HTML widgets

## [v2.0.0] - Previous Release

### ✨ Features
- 🌙 Dark mode support
- 🔍 Advanced search functionality  
- 🔎 Zoom controls (50% - 300%)
- 📚 Recent files menu
- 🎨 Modern interface design
- 📝 File validation
- 📊 Logging system
- 💾 Persistent configuration
