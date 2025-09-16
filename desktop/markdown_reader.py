#!/usr/bin/env python3
"""
Leitor MD - Markdown Reader with PDF Export
A simple markdown file viewer with PDF export functionality
"""

import os
import sys
import logging
import json
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, Toplevel, Scrollbar, Entry, Button, Frame, Label, Scale, Checkbutton, BooleanVar
from tkinter import ttk
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pathlib import Path
try:
    import weasyprint
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError):
    WEASYPRINT_AVAILABLE = False
    
if not WEASYPRINT_AVAILABLE:
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        REPORTLAB_AVAILABLE = True
    except ImportError:
        REPORTLAB_AVAILABLE = False
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='md_reader.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Configuration file path
CONFIG_FILE = 'md_reader_config.json'

def load_config():
    """Load application configuration"""
    default_config = {
        'dark_mode': False,
        'zoom_level': 1.0,
        'recent_files': [],
        'window_geometry': '1000x700',
        'show_line_numbers': False
    }

    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                default_config.update(config)
    except Exception as e:
        logger.error(f"Error loading config: {str(e)}")

    return default_config

def save_config(config):
    """Save application configuration"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        logger.info("Configuration saved successfully")
    except Exception as e:
        logger.error(f"Error saving config: {str(e)}")

try:
    from tkinterweb import HtmlFrame
    TKINTERWEB_AVAILABLE = True
except ImportError:
    TKINTERWEB_AVAILABLE = False


class MarkdownReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Leitor MD - Markdown Reader")
        self.root.geometry("1000x700")
        self.root.minsize(600, 400)

        # Load configuration
        self.config = load_config()

        # Apply saved geometry
        if 'window_geometry' in self.config:
            self.root.geometry(self.config['window_geometry'])

        # Current file path
        self.current_file = None

        # Supported file extensions
        self.supported_extensions = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn'}

        # UI state
        self.dark_mode = self.config.get('dark_mode', False)
        self.zoom_level = self.config.get('zoom_level', 1.0)
        self.search_window = None
        self.search_results = []
        self.current_search_index = 0

        # Apply dark mode if enabled
        if self.dark_mode:
            self.apply_dark_mode()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Create GUI
        self.create_menu()
        self.create_widgets()
        
        # Configure markdown processor
        self.md = markdown.Markdown(
            extensions=['codehilite', 'tables', 'fenced_code', 'toc'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )
        
    def validate_file(self, filepath):
        """Validate if file exists and is a supported markdown file"""
        try:
            path = Path(filepath)
            if not path.exists():
                logger.error(f"File not found: {filepath}")
                return False, "Arquivo não encontrado"

            if not path.is_file():
                logger.error(f"Not a file: {filepath}")
                return False, "Caminho não é um arquivo"

            if path.suffix.lower() not in self.supported_extensions:
                logger.error(f"Unsupported file type: {filepath}")
                return False, f"Tipo de arquivo não suportado. Use: {', '.join(self.supported_extensions)}"

            # Check if file is readable
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    # Try to read first few bytes
                    f.read(100)
            except UnicodeDecodeError:
                logger.error(f"File encoding error: {filepath}")
                return False, "Arquivo não está em formato UTF-8"
            except Exception as e:
                logger.error(f"File read error: {filepath} - {str(e)}")
                return False, f"Erro ao ler arquivo: {str(e)}"

            logger.info(f"File validated successfully: {filepath}")
            return True, "Arquivo válido"

        except Exception as e:
            logger.error(f"Validation error: {filepath} - {str(e)}")
            return False, f"Erro na validação: {str(e)}"

    def create_menu(self):
        """Create the application menu"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir...", command=self.open_file, accelerator="Ctrl+O")

        # Recent files submenu
        self.recent_menu = Menu(file_menu, tearoff=0)
        file_menu.add_cascade(label="Arquivos Recentes", menu=self.recent_menu)
        self.update_recent_menu()

        file_menu.add_separator()
        file_menu.add_command(label="Exportar como PDF...", command=self.export_pdf, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit, accelerator="Ctrl+Q")

        # View menu
        view_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Visualizar", menu=view_menu)
        view_menu.add_command(label="Buscar...", command=self.open_search, accelerator="Ctrl+F")
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Modo Escuro", command=self.toggle_dark_mode,
                                 variable=BooleanVar(value=self.dark_mode))
        view_menu.add_separator()
        view_menu.add_command(label="Aumentar Zoom", command=self.zoom_in, accelerator="Ctrl++")
        view_menu.add_command(label="Diminuir Zoom", command=self.zoom_out, accelerator="Ctrl+-")
        view_menu.add_command(label="Zoom Normal", command=self.reset_zoom, accelerator="Ctrl+0")

        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)

        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-e>', lambda e: self.export_pdf())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<Control-f>', lambda e: self.open_search())
        self.root.bind('<Control-plus>', lambda e: self.zoom_in())
        self.root.bind('<Control-minus>', lambda e: self.zoom_out())
        self.root.bind('<Control-0>', lambda e: self.reset_zoom())
        
    def create_widgets(self):
        """Create the main widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))

        # File operations
        ttk.Button(toolbar, text="Abrir Arquivo", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Exportar PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Search button
        ttk.Button(toolbar, text="Buscar", command=self.open_search).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # Zoom controls
        ttk.Label(toolbar, text="Zoom:").pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="-", command=self.zoom_out, width=3).pack(side=tk.LEFT, padx=(0, 2))
        self.zoom_label = ttk.Label(toolbar, text=f"{int(self.zoom_level * 100)}%")
        self.zoom_label.pack(side=tk.LEFT, padx=(0, 2))
        ttk.Button(toolbar, text="+", command=self.zoom_in, width=3).pack(side=tk.LEFT, padx=(0, 10))

        # Dark mode toggle
        self.dark_mode_var = BooleanVar(value=self.dark_mode)
        ttk.Checkbutton(toolbar, text="Modo Escuro", variable=self.dark_mode_var,
                       command=self.toggle_dark_mode).pack(side=tk.LEFT, padx=(0, 10))

        # File path label
        self.file_label = ttk.Label(toolbar, text="Nenhum arquivo carregado", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Content area
        if TKINTERWEB_AVAILABLE:
            # Use HTML widget if available
            self.html_frame = HtmlFrame(main_frame, messages_enabled=False)
            self.html_frame.pack(fill=tk.BOTH, expand=True)
        else:
            # Fallback to text widget
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            # Scrollbars
            v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
            h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
            
            # Text widget
            self.text_widget = tk.Text(
                text_frame, 
                wrap=tk.WORD, 
                yscrollcommand=v_scrollbar.set,
                xscrollcommand=h_scrollbar.set,
                font=('Arial', 11),
                padx=10,
                pady=10
            )
            
            v_scrollbar.config(command=self.text_widget.yview)
            h_scrollbar.config(command=self.text_widget.xview)
            
            # Grid layout
            self.text_widget.grid(row=0, column=0, sticky='nsew')
            v_scrollbar.grid(row=0, column=1, sticky='ns')
            h_scrollbar.grid(row=1, column=0, sticky='ew')
            
            text_frame.grid_rowconfigure(0, weight=1)
            text_frame.grid_columnconfigure(0, weight=1)
        
    def open_file(self, filepath=None):
        """Open and display a markdown file"""
        if filepath is None:
            filepath = filedialog.askopenfilename(
                title="Abrir arquivo Markdown",
                filetypes=[
                    ("Markdown files", "*.md *.markdown *.mdown *.mkd *.mkdn"),
                    ("All files", "*.*")
                ]
            )

        if filepath:
            # Validate file before opening
            is_valid, message = self.validate_file(filepath)
            if not is_valid:
                messagebox.showerror("Erro de Validação", message)
                return

            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()

                self.current_file = filepath
                self.display_markdown(content)
                self.update_title(filepath)
                self.add_to_recent_files(filepath)
                logger.info(f"File opened successfully: {filepath}")

            except Exception as e:
                logger.error(f"Error opening file: {filepath} - {str(e)}")
                messagebox.showerror("Erro", f"Erro ao abrir arquivo:\n{str(e)}")
    
    def display_markdown(self, markdown_content):
        """Display markdown content"""
        # Convert markdown to HTML
        html_content = self.md.convert(markdown_content)
        
        # Create complete HTML document with CSS
        full_html = self.create_html_document(html_content)
        
        if TKINTERWEB_AVAILABLE:
            # Display in HTML widget
            self.html_frame.load_html(full_html)
        else:
            # Display plain text in text widget (fallback)
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert('1.0', markdown_content)
    
    def create_html_document(self, html_content):
        """Create a complete HTML document with CSS styling"""
        # Dynamic styling based on current mode and zoom
        if self.dark_mode:
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
        
        # Calculate font size based on zoom level
        base_font_size = int(16 * self.zoom_level)
        small_font_size = int(14 * self.zoom_level)
        code_font_size = int(13 * self.zoom_level)
        
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
    
    def export_pdf(self):
        """Export current markdown as PDF"""
        if not self.current_file:
            messagebox.showwarning("Aviso", "Nenhum arquivo carregado para exportar.")
            return
        
        # Check if any PDF library is available
        if not WEASYPRINT_AVAILABLE and not REPORTLAB_AVAILABLE:
            messagebox.showerror(
                "Erro", 
                "Nenhuma biblioteca de PDF disponível.\n\n"
                "Instale uma das seguintes:\n"
                "- pip install weasyprint (requer GTK no Windows)\n"
                "- pip install reportlab"
            )
            return
        
        # Get save path
        default_name = Path(self.current_file).stem + ".pdf"
        filepath = filedialog.asksaveasfilename(
            title="Exportar como PDF",
            defaultextension=".pdf",
            initialfile=default_name,
            filetypes=[("PDF files", "*.pdf")]
        )
        
        if filepath:
            try:
                # Read markdown content
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    markdown_content = file.read()
                
                if WEASYPRINT_AVAILABLE:
                    # Use WeasyPrint if available
                    html_content = self.md.convert(markdown_content)
                    full_html = self.create_html_document(html_content)
                    document = weasyprint.HTML(string=full_html)
                    document.write_pdf(filepath)
                elif REPORTLAB_AVAILABLE:
                    # Use ReportLab as fallback
                    self.export_pdf_reportlab(markdown_content, filepath)
                else:
                    # HTML fallback when no PDF library is available
                    self.export_html_fallback(markdown_content, filepath)
                    return
                
                messagebox.showinfo("Sucesso", f"PDF exportado com sucesso:\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar PDF:\n{str(e)}")
    
    def export_pdf_reportlab(self, markdown_content, filepath):
        """Export PDF using ReportLab with improved HTML conversion"""
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
        import re
        from html.parser import HTMLParser
        from io import StringIO

        # Create document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)

        # Create enhanced styles
        styles = getSampleStyleSheet()

        # Add custom styles
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=18,
            spaceAfter=12,
            textColor=colors.darkblue
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading1',
            parent=styles['Heading1'],
            fontSize=14,
            spaceAfter=10,
            textColor=colors.darkblue
        ))

        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=12,
            spaceAfter=8,
            textColor=colors.darkblue
        ))

        styles.add(ParagraphStyle(
            name='CodeStyle',
            parent=styles['Code'],
            fontSize=9,
            backgroundColor=colors.lightgrey,
            borderColor=colors.grey,
            borderWidth=1,
            leftIndent=20,
            rightIndent=20,
            spaceBefore=6,
            spaceAfter=6
        ))

        styles.add(ParagraphStyle(
            name='Blockquote',
            parent=styles['Normal'],
            leftIndent=20,
            rightIndent=20,
            textColor=colors.grey,
            borderColor=colors.lightgrey,
            borderWidth=1,
            borderPadding=5
        ))

        story = []

        # Convert markdown to HTML first, then parse HTML
        html_content = self.md.convert(markdown_content)

        # Simple HTML parser for ReportLab
        class ReportLabHTMLParser(HTMLParser):
            def __init__(self, story, styles):
                super().__init__()
                self.story = story
                self.styles = styles
                self.current_text = []
                self.in_code = False
                self.in_blockquote = False
                self.in_list = False
                self.list_items = []

            def handle_data(self, data):
                self.current_text.append(data)

            def handle_starttag(self, tag, attrs):
                text = ''.join(self.current_text).strip()
                if text:
                    self.add_text(text)
                self.current_text = []

                if tag == 'h1':
                    self.story.append(Spacer(1, 12))
                elif tag == 'h2':
                    self.story.append(Spacer(1, 10))
                elif tag == 'h3':
                    self.story.append(Spacer(1, 8))
                elif tag == 'pre' or tag == 'code':
                    self.in_code = True
                elif tag == 'blockquote':
                    self.in_blockquote = True
                elif tag == 'ul' or tag == 'ol':
                    self.in_list = True
                    self.list_items = []

            def handle_endtag(self, tag):
                text = ''.join(self.current_text).strip()
                if text:
                    self.add_text(text)
                self.current_text = []

                if tag == 'h1':
                    if text:
                        self.story.append(Paragraph(text, self.styles['CustomTitle']))
                    self.story.append(Spacer(1, 6))
                elif tag == 'h2':
                    if text:
                        self.story.append(Paragraph(text, self.styles['CustomHeading1']))
                    self.story.append(Spacer(1, 6))
                elif tag == 'h3':
                    if text:
                        self.story.append(Paragraph(text, self.styles['CustomHeading2']))
                    self.story.append(Spacer(1, 6))
                elif tag == 'p':
                    if text and not self.in_code and not self.in_blockquote:
                        self.story.append(Paragraph(text, self.styles['Normal']))
                        self.story.append(Spacer(1, 6))
                elif tag == 'pre' or tag == 'code':
                    if text and self.in_code:
                        self.story.append(Paragraph(text, self.styles['CodeStyle']))
                        self.story.append(Spacer(1, 6))
                    self.in_code = False
                elif tag == 'blockquote':
                    if text and self.in_blockquote:
                        self.story.append(Paragraph(text, self.styles['Blockquote']))
                        self.story.append(Spacer(1, 6))
                    self.in_blockquote = False
                elif tag == 'ul' or tag == 'ol':
                    # Add list items
                    for item in self.list_items:
                        bullet = '• ' if tag == 'ul' else f'{len(self.list_items) - self.list_items.index(item)}. '
                        self.story.append(Paragraph(bullet + item, self.styles['Normal']))
                    self.in_list = False
                    self.story.append(Spacer(1, 6))
                elif tag == 'li':
                    if text:
                        self.list_items.append(text)

            def add_text(self, text):
                if self.in_code or self.in_blockquote:
                    self.current_text.append(text)
                elif not self.in_list:
                    self.current_text.append(text)

            def handle_complete(self):
                # Add any remaining text
                text = ''.join(self.current_text).strip()
                if text:
                    self.story.append(Paragraph(text, self.styles['Normal']))

        # Parse HTML and build PDF
        parser = ReportLabHTMLParser(story, styles)
        parser.feed(html_content)
        parser.handle_complete()

        # Build PDF
        try:
            doc.build(story)
            logger.info(f"PDF exported successfully using ReportLab: {filepath}")
        except Exception as e:
            logger.error(f"PDF export failed: {filepath} - {str(e)}")
            raise
    
    def export_html_fallback(self, markdown_content, filepath):
        """Export as HTML file if no PDF library is available"""
        html_content = self.md.convert(markdown_content)
        full_html = self.create_html_document(html_content)
        
        html_filepath = filepath.replace('.pdf', '.html')
        with open(html_filepath, 'w', encoding='utf-8') as f:
            f.write(full_html)
        
        messagebox.showinfo(
            "Aviso", 
            f"PDF não disponível. Arquivo exportado como HTML:\n{html_filepath}\n\n"
            "Para exportar PDF, instale:\npip install reportlab"
        )
    
    def update_title(self, filepath):
        """Update window title and file label"""
        filename = Path(filepath).name
        self.root.title(f"Leitor MD - {filename}")
        self.file_label.config(text=f"Arquivo: {filename}", foreground="black")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "Sobre",
            "Leitor MD - Markdown Reader\n\n"
            "Um leitor simples de arquivos Markdown com exportação para PDF\n\n"
            "Versão 2.0\n"
            "Desenvolvido com Python e Tkinter\n\n"
            "Recursos:\n"
            "• Modo escuro\n"
            "• Busca de texto\n"
            "• Zoom\n"
            "• Arquivos recentes\n"
            "• Exportação PDF aprimorada"
        )

    def toggle_dark_mode(self):
        """Toggle dark mode"""
        self.dark_mode = not self.dark_mode
        self.config['dark_mode'] = self.dark_mode
        self.dark_mode_var.set(self.dark_mode)

        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()

        logger.info(f"Dark mode {'enabled' if self.dark_mode else 'disabled'}")

    def apply_dark_mode(self):
        """Apply dark mode styling"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except:
            pass

        # Configure dark mode colors
        bg_color = '#2b2b2b'
        fg_color = '#ffffff'
        select_bg = '#404040'

        self.root.configure(bg=bg_color)

        # Update ttk styles
        style.configure('TFrame', background=bg_color)
        style.configure('TLabel', background=bg_color, foreground=fg_color)
        style.configure('TButton', background=select_bg, foreground=fg_color)
        style.configure('TCheckbutton', background=bg_color, foreground=fg_color)

        # Update existing widgets
        for widget in self.root.winfo_children():
            self._update_widget_colors(widget, bg_color, fg_color)

        # Update content area background
        if hasattr(self, 'text_widget'):
            self.text_widget.configure(bg=bg_color, fg=fg_color)
        
        # Refresh content to apply new styling for HTML widget
        if hasattr(self, 'html_frame') and TKINTERWEB_AVAILABLE:
            self.refresh_content()

    def apply_light_mode(self):
        """Apply light mode styling"""
        style = ttk.Style()
        try:
            style.theme_use('default')
        except:
            pass

        # Default colors will be used
        self.root.configure(bg='#ffffff')

        # Reset content area background
        if hasattr(self, 'text_widget'):
            self.text_widget.configure(bg='#ffffff', fg='#000000')
        
        # Refresh content to apply new styling for HTML widget
        if hasattr(self, 'html_frame') and TKINTERWEB_AVAILABLE:
            self.refresh_content()

    def _update_widget_colors(self, widget, bg_color, fg_color):
        """Recursively update widget colors"""
        try:
            if isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button, ttk.Checkbutton)):
                widget.configure(background=bg_color, foreground=fg_color)
            elif isinstance(widget, tk.Label):
                widget.configure(bg=bg_color, fg=fg_color)
        except:
            pass

        for child in widget.winfo_children():
            self._update_widget_colors(child, bg_color, fg_color)

    def zoom_in(self):
        """Increase zoom level"""
        self.zoom_level = min(self.zoom_level + 0.1, 3.0)
        self.update_zoom()

    def zoom_out(self):
        """Decrease zoom level"""
        self.zoom_level = max(self.zoom_level - 0.1, 0.5)
        self.update_zoom()

    def reset_zoom(self):
        """Reset zoom to default"""
        self.zoom_level = 1.0
        self.update_zoom()

    def update_zoom(self):
        """Update zoom level"""
        self.config['zoom_level'] = self.zoom_level
        self.zoom_label.config(text=f"{int(self.zoom_level * 100)}%")

        if hasattr(self, 'html_frame') and TKINTERWEB_AVAILABLE:
            # For HTML widget, update font size via CSS
            self.refresh_content()
        elif hasattr(self, 'text_widget'):
            # For text widget, update font size
            current_font = self.text_widget['font']
            font_size = int(11 * self.zoom_level)
            self.text_widget.configure(font=('Arial', font_size))

        logger.info(f"Zoom level set to {int(self.zoom_level * 100)}%")

    def open_search(self):
        """Open search dialog"""
        if self.search_window:
            self.search_window.lift()
            return

        self.search_window = Toplevel(self.root)
        self.search_window.title("Buscar")
        self.search_window.geometry("400x150")
        self.search_window.resizable(False, False)

        # Center the window
        self.search_window.transient(self.root)

        # Search frame
        search_frame = ttk.Frame(self.search_window, padding="10")
        search_frame.pack(fill=tk.BOTH, expand=True)

        # Search entry
        ttk.Label(search_frame, text="Buscar:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        self.search_entry = Entry(search_frame, width=40)
        self.search_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 5))
        self.search_entry.bind('<Return>', lambda e: self.perform_search())
        self.search_entry.bind('<KeyRelease>', lambda e: self.perform_search())

        # Search options
        self.case_sensitive_var = BooleanVar(value=False)
        ttk.Checkbutton(search_frame, text="Diferenciar maiúsculas/minúsculas",
                       variable=self.case_sensitive_var).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Navigation buttons
        nav_frame = ttk.Frame(search_frame)
        nav_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))

        ttk.Button(nav_frame, text="Anterior", command=self.search_previous).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(nav_frame, text="Próximo", command=self.search_next).pack(side=tk.LEFT, padx=(0, 5))

        # Results label
        self.search_results_label = ttk.Label(nav_frame, text="")
        self.search_results_label.pack(side=tk.LEFT, padx=(10, 0))

        # Close button
        ttk.Button(search_frame, text="Fechar", command=self.close_search).grid(row=3, column=0, columnspan=3, pady=(10, 0))

        # Focus on search entry
        self.search_entry.focus()

        # Bind window close event
        self.search_window.protocol("WM_DELETE_WINDOW", self.close_search)

    def perform_search(self):
        """Perform search in current content"""
        search_text = self.search_entry.get()
        if not search_text:
            self.search_results = []
            self.current_search_index = 0
            self.search_results_label.config(text="")
            return

        try:
            # Get current content
            if hasattr(self, 'html_frame') and TKINTERWEB_AVAILABLE:
                # For HTML widget, get HTML content
                content = self.get_current_markdown_content()
            elif hasattr(self, 'text_widget'):
                # For text widget, get text content
                content = self.text_widget.get('1.0', tk.END)

            # Perform search
            import re
            flags = 0 if self.case_sensitive_var.get() else re.IGNORECASE
            pattern = re.compile(re.escape(search_text), flags)

            self.search_results = []
            for match in pattern.finditer(content):
                self.search_results.append(match.start())

            self.current_search_index = 0
            self.update_search_display()

        except Exception as e:
            logger.error(f"Search error: {str(e)}")

    def search_next(self):
        """Navigate to next search result"""
        if not self.search_results:
            return

        self.current_search_index = (self.current_search_index + 1) % len(self.search_results)
        self.update_search_display()

    def search_previous(self):
        """Navigate to previous search result"""
        if not self.search_results:
            return

        self.current_search_index = (self.current_search_index - 1) % len(self.search_results)
        self.update_search_display()

    def update_search_display(self):
        """Update search result display"""
        if not self.search_results:
            self.search_results_label.config(text="Nenhum resultado")
            return

        result_text = f"Resultado {self.current_search_index + 1} de {len(self.search_results)}"
        self.search_results_label.config(text=result_text)

        # Highlight the current result (simplified - would need more complex implementation for HTML widget)
        if hasattr(self, 'text_widget'):
            pos = self.search_results[self.current_search_index]
            line_num = self.text_widget.index(f'1.0+{pos}c').split('.')[0]
            self.text_widget.see(f'{line_num}.0')

    def close_search(self):
        """Close search dialog"""
        if self.search_window:
            self.search_window.destroy()
            self.search_window = None

    def get_current_markdown_content(self):
        """Get current markdown content"""
        if self.current_file:
            try:
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    return file.read()
            except:
                return ""
        return ""

    def refresh_content(self):
        """Refresh content display"""
        if self.current_file:
            try:
                with open(self.current_file, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.display_markdown(content)
            except Exception as e:
                logger.error(f"Error refreshing content: {str(e)}")

    def update_recent_menu(self):
        """Update recent files menu"""
        self.recent_menu.delete(0, tk.END)

        recent_files = self.config.get('recent_files', [])
        if not recent_files:
            self.recent_menu.add_command(label="Nenhum arquivo recente", state=tk.DISABLED)
        else:
            for i, filepath in enumerate(recent_files[:10]):  # Show max 10 recent files
                filename = os.path.basename(filepath)
                self.recent_menu.add_command(
                    label=f"{i+1}. {filename}",
                    command=lambda f=filepath: self.open_recent_file(f)
                )

        # Clear recent files option
        if recent_files:
            self.recent_menu.add_separator()
            self.recent_menu.add_command(label="Limpar Lista", command=self.clear_recent_files)

    def open_recent_file(self, filepath):
        """Open a recent file"""
        if os.path.exists(filepath):
            self.open_file(filepath)
        else:
            # Remove from recent files if it doesn't exist
            self.remove_from_recent_files(filepath)

    def add_to_recent_files(self, filepath):
        """Add file to recent files list"""
        recent_files = self.config.get('recent_files', [])

        # Remove if already exists
        if filepath in recent_files:
            recent_files.remove(filepath)

        # Add to beginning
        recent_files.insert(0, filepath)

        # Keep only last 20 files
        recent_files = recent_files[:20]

        self.config['recent_files'] = recent_files
        self.update_recent_menu()

    def remove_from_recent_files(self, filepath):
        """Remove file from recent files list"""
        recent_files = self.config.get('recent_files', [])
        if filepath in recent_files:
            recent_files.remove(filepath)
            self.config['recent_files'] = recent_files
            self.update_recent_menu()

    def clear_recent_files(self):
        """Clear recent files list"""
        self.config['recent_files'] = []
        self.update_recent_menu()

    def on_closing(self):
        """Handle window closing"""
        # Save window geometry
        self.config['window_geometry'] = self.root.geometry()

        # Save configuration
        save_config(self.config)

        # Destroy window
        self.root.destroy()


def main():
    """Main function"""
    root = tk.Tk()
    app = MarkdownReader(root)
    
    # Check if a file was passed as argument
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        if os.path.exists(filepath) and filepath.lower().endswith(('.md', '.markdown', '.mdown', '.mkd', '.mkdn')):
            app.open_file(filepath)
    
    root.mainloop()


if __name__ == "__main__":
    main()
