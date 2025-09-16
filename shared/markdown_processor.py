#!/usr/bin/env python3
"""
Shared Markdown Processing Module
Core functionality for processing markdown files across platforms
"""

import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class MarkdownProcessor:
    """Cross-platform markdown processor with consistent styling"""
    
    def __init__(self):
        """Initialize the markdown processor with extensions"""
        self.md = markdown.Markdown(
            extensions=['codehilite', 'tables', 'fenced_code', 'toc'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )
    
    def convert_to_html(self, markdown_content: str) -> str:
        """Convert markdown content to HTML"""
        try:
            return self.md.convert(markdown_content)
        except Exception as e:
            logger.error(f"Error converting markdown to HTML: {e}")
            return f"<p>Error processing markdown: {e}</p>"
    
    def create_styled_html(self, html_content: str, dark_mode: bool = False, zoom_level: float = 1.0) -> str:
        """Create complete HTML document with dynamic styling"""
        
        # Dynamic styling based on theme and zoom
        if dark_mode:
            bg_color = '#2b2b2b'
            text_color = '#ffffff'
            border_color = '#404040'
            code_bg = '#363636'
            table_bg = '#363636'
            table_alternate = '#404040'
            link_color = '#7db7ff'
        else:
            bg_color = '#ffffff'
            text_color = '#333333'
            border_color = '#eaecef'
            code_bg = '#f6f8fa'
            table_bg = '#f6f8fa'
            table_alternate = '#f6f8fa'
            link_color = '#0366d6'
        
        # Calculate font sizes based on zoom level
        base_font_size = int(16 * zoom_level)
        code_font_size = int(13 * zoom_level)
        
        css_style = f"""
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: {text_color};
                max-width: none;
                margin: 0;
                padding: 20px;
                background-color: {bg_color};
                font-size: {base_font_size}px;
            }}
            h1, h2, h3, h4, h5, h6 {{
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
            }}
            h1 {{ border-bottom: 1px solid {border_color}; padding-bottom: 10px; }}
            h2 {{ border-bottom: 1px solid {border_color}; padding-bottom: 8px; }}
            code {{
                background-color: {code_bg};
                border-radius: 3px;
                font-size: {code_font_size}px;
                margin: 0;
                padding: .2em .4em;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
                color: {text_color};
            }}
            pre {{
                background-color: {code_bg};
                border-radius: 6px;
                font-size: {code_font_size}px;
                line-height: 1.45;
                overflow: auto;
                padding: 16px;
                color: {text_color};
            }}
            pre code {{
                background-color: transparent;
                border: 0;
                display: inline;
                line-height: inherit;
                margin: 0;
                overflow: visible;
                padding: 0;
                word-wrap: normal;
            }}
            blockquote {{
                border-left: 4px solid {border_color};
                color: {text_color};
                opacity: 0.8;
                margin: 0;
                padding: 0 16px;
            }}
            table {{
                border-collapse: collapse;
                border-spacing: 0;
                width: 100%;
                margin: 16px 0;
            }}
            table th, table td {{
                border: 1px solid {border_color};
                padding: 6px 13px;
                color: {text_color};
            }}
            table th {{
                background-color: {table_bg};
                font-weight: 600;
            }}
            table tr:nth-child(2n) {{
                background-color: {table_alternate};
            }}
            img {{
                max-width: 100%;
                height: auto;
            }}
            a {{
                color: {link_color};
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
        </style>
        """
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Markdown Preview</title>
            {css_style}
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
    
    def process_file(self, filepath: str, dark_mode: bool = False, zoom_level: float = 1.0) -> str:
        """Process a markdown file and return styled HTML"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            html_content = self.convert_to_html(markdown_content)
            return self.create_styled_html(html_content, dark_mode, zoom_level)
            
        except Exception as e:
            logger.error(f"Error processing file {filepath}: {e}")
            return self.create_styled_html(f"<p>Error loading file: {e}</p>", dark_mode, zoom_level)

# Utility functions for file validation
class FileValidator:
    """Cross-platform file validation utilities"""
    
    SUPPORTED_EXTENSIONS = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn'}
    
    @classmethod
    def is_supported_file(cls, filepath: str) -> bool:
        """Check if file extension is supported"""
        return Path(filepath).suffix.lower() in cls.SUPPORTED_EXTENSIONS
    
    @classmethod
    def validate_file(cls, filepath: str) -> tuple[bool, str]:
        """Validate if file exists and is supported"""
        try:
            path = Path(filepath)
            
            if not path.exists():
                return False, "File not found"
            
            if not path.is_file():
                return False, "Path is not a file"
            
            if not cls.is_supported_file(filepath):
                return False, f"Unsupported file type. Supported: {', '.join(cls.SUPPORTED_EXTENSIONS)}"
            
            # Test if file is readable
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    f.read(100)  # Test read first 100 chars
            except UnicodeDecodeError:
                return False, "File is not UTF-8 encoded"
            except Exception as e:
                return False, f"Cannot read file: {e}"
            
            return True, "File is valid"
            
        except Exception as e:
            return False, f"Validation error: {e}"
