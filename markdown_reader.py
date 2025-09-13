#!/usr/bin/env python3
"""
Leitor MD - Markdown Reader with PDF Export
A simple markdown file viewer with PDF export functionality
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, Menu
from tkinter import ttk
import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
# import weasyprint  # Disabled due to Windows GTK dependency issues
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
from pathlib import Path

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
        
        # Current file path
        self.current_file = None
        
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
        
    def create_menu(self):
        """Create the application menu"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=file_menu)
        file_menu.add_command(label="Abrir...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Exportar como PDF...", command=self.export_pdf, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Help menu
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Sobre", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-e>', lambda e: self.export_pdf())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
    def create_widgets(self):
        """Create the main widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Toolbar
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(toolbar, text="Abrir Arquivo", command=self.open_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(toolbar, text="Exportar PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=(0, 5))
        
        # File path label
        self.file_label = ttk.Label(toolbar, text="Nenhum arquivo carregado", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=(10, 0))
        
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
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.current_file = filepath
                self.display_markdown(content)
                self.update_title(filepath)
                
            except Exception as e:
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
        css_style = """
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: none;
                margin: 0;
                padding: 20px;
                background-color: #fff;
            }
            h1, h2, h3, h4, h5, h6 {
                margin-top: 24px;
                margin-bottom: 16px;
                font-weight: 600;
                line-height: 1.25;
            }
            h1 { border-bottom: 1px solid #eaecef; padding-bottom: 10px; }
            h2 { border-bottom: 1px solid #eaecef; padding-bottom: 8px; }
            code {
                background-color: rgba(27,31,35,.05);
                border-radius: 3px;
                font-size: 85%;
                margin: 0;
                padding: .2em .4em;
                font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            }
            pre {
                background-color: #f6f8fa;
                border-radius: 6px;
                font-size: 85%;
                line-height: 1.45;
                overflow: auto;
                padding: 16px;
            }
            pre code {
                background-color: transparent;
                border: 0;
                display: inline;
                line-height: inherit;
                margin: 0;
                overflow: visible;
                padding: 0;
                word-wrap: normal;
            }
            blockquote {
                border-left: 4px solid #dfe2e5;
                color: #6a737d;
                margin: 0;
                padding: 0 16px;
            }
            table {
                border-collapse: collapse;
                border-spacing: 0;
                width: 100%;
                margin: 16px 0;
            }
            table th, table td {
                border: 1px solid #dfe2e5;
                padding: 6px 13px;
            }
            table th {
                background-color: #f6f8fa;
                font-weight: 600;
            }
            table tr:nth-child(2n) {
                background-color: #f6f8fa;
            }
            img {
                max-width: 100%;
                height: auto;
            }
            a {
                color: #0366d6;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
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
                    # HTML fallback
                    self.export_html_fallback(markdown_content, filepath)
                
                messagebox.showinfo("Sucesso", f"PDF exportado com sucesso:\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar PDF:\n{str(e)}")
    
    def export_pdf_reportlab(self, markdown_content, filepath):
        """Export PDF using ReportLab (simpler but less formatting)"""
        from io import StringIO
        import re
        
        # Create document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Create styles
        styles = getSampleStyleSheet()
        story = []
        
        # Parse markdown content line by line
        lines = markdown_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                story.append(Spacer(1, 12))
                continue
            
            # Headers
            if line.startswith('# '):
                text = line[2:].strip()
                story.append(Paragraph(text, styles['Title']))
                story.append(Spacer(1, 12))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, styles['Heading1']))
                story.append(Spacer(1, 12))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, styles['Heading2']))
                story.append(Spacer(1, 12))
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                text = '• ' + line[2:].strip()
                story.append(Paragraph(text, styles['Normal']))
            elif re.match(r'^\d+\. ', line):
                text = line.strip()
                story.append(Paragraph(text, styles['Normal']))
            # Code blocks (simple)
            elif line.startswith('```'):
                story.append(Paragraph('[Bloco de código]', styles['Code']))
            # Regular paragraphs
            else:
                # Handle bold and italic (basic)
                # Handle bold and italic with regex to ensure correct tag pairing
                # Process bold first
                text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                # Then process italic
                text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
                story.append(Paragraph(text, styles['Normal']))
            
            story.append(Spacer(1, 6))
        
        # Build PDF
        doc.build(story)
    
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
            "Versão 1.0\n"
            "Desenvolvido com Python e Tkinter"
        )


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
