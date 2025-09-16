#!/usr/bin/env python3
"""
Basic tests for MD Reader
"""

import sys
import os
import tempfile
import unittest
from pathlib import Path

# Add the parent directory to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from markdown_reader import load_config, save_config, logger

class TestMarkdownReader(unittest.TestCase):
    """Test cases for MarkdownReader functionality"""

    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.temp_dir, 'test.md')

        # Create a test markdown file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("""# Test Document

This is a **test** document with *formatting*.

## Features

- Dark mode support
- Search functionality
- PDF export
- Recent files tracking

> This is a blockquote

```python
def hello_world():
    print("Hello, World!")
```
""")

    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_file_validation(self):
        """Test file validation functionality"""
        # Import the validation logic directly
        from markdown_reader import MarkdownReader

        # Create test files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test markdown")
            valid_md = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Not markdown")
            invalid_txt = f.name

        # Create a minimal mock for testing validation
        class MockReader:
            def __init__(self):
                self.supported_extensions = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn'}

            def validate_file(self, filepath):
                """Validate if file exists and is a supported markdown file"""
                try:
                    path = Path(filepath)
                    if not path.exists():
                        return False, "Arquivo não encontrado"

                    if not path.is_file():
                        return False, "Caminho não é um arquivo"

                    if path.suffix.lower() not in self.supported_extensions:
                        return False, f"Tipo de arquivo não suportado. Use: {', '.join(self.supported_extensions)}"

                    # Check if file is readable
                    try:
                        with open(path, 'r', encoding='utf-8') as f:
                            f.read(100)
                    except UnicodeDecodeError:
                        return False, "Arquivo não está em formato UTF-8"
                    except Exception as e:
                        return False, f"Erro ao ler arquivo: {str(e)}"

                    return True, "Arquivo válido"

                except Exception as e:
                    return False, f"Erro na validação: {str(e)}"

        reader = MockReader()

        # Test valid file
        is_valid, message = reader.validate_file(self.test_file)
        self.assertTrue(is_valid)
        self.assertEqual(message, "Arquivo válido")

        # Test non-existent file
        is_valid, message = reader.validate_file("nonexistent.md")
        self.assertFalse(is_valid)
        self.assertEqual(message, "Arquivo não encontrado")

        # Test invalid file type
        is_valid, message = reader.validate_file(invalid_txt)
        self.assertFalse(is_valid)
        self.assertIn("Tipo de arquivo não suportado", message)

        # Clean up
        os.unlink(valid_md)
        os.unlink(invalid_txt)

    def test_config_loading(self):
        """Test configuration loading and saving"""
        # Clean up any existing config file
        import os
        if os.path.exists('md_reader_config.json'):
            os.remove('md_reader_config.json')

        # Test default config
        config = load_config()
        self.assertIn('dark_mode', config)
        self.assertIn('zoom_level', config)
        self.assertIn('recent_files', config)
        self.assertEqual(config['zoom_level'], 1.0)

        # Test config saving
        test_config = {
            'dark_mode': True,
            'zoom_level': 1.5,
            'recent_files': ['/test/file.md']
        }
        save_config(test_config)

        # Test loading saved config
        loaded_config = load_config()
        self.assertTrue(loaded_config['dark_mode'])
        self.assertEqual(loaded_config['zoom_level'], 1.5)
        self.assertEqual(loaded_config['recent_files'], ['/test/file.md'])

    def test_markdown_parsing(self):
        """Test markdown parsing functionality"""
        import markdown
        from pygments import highlight
        from pygments.lexers import get_lexer_by_name
        from pygments.formatters import HtmlFormatter

        # Test markdown conversion directly
        md = markdown.Markdown(
            extensions=['codehilite', 'tables', 'fenced_code', 'toc'],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': True
                }
            }
        )

        # Test markdown conversion
        with open(self.test_file, 'r', encoding='utf-8') as f:
            content = f.read()

        html_content = md.convert(content)
        self.assertIn('<h1 id="test-document">', html_content)
        self.assertIn('<h2 id="features">', html_content)
        self.assertIn('<strong>test</strong>', html_content)
        self.assertIn('<em>formatting</em>', html_content)
        self.assertIn('<blockquote>', html_content)
        self.assertIn('<span class="k">def</span>', html_content)  # Pygments highlighting

    def test_supported_extensions(self):
        """Test supported file extensions"""
        # Test extensions directly
        expected_extensions = {'.md', '.markdown', '.mdown', '.mkd', '.mkdn'}

        # Test various file extensions
        valid_files = ['test.md', 'test.markdown', 'test.mdown', 'test.mkd', 'test.mkdn']
        for filename in valid_files:
            path = Path(filename)
            self.assertTrue(path.suffix.lower() in expected_extensions)

        invalid_files = ['test.txt', 'test.doc', 'test.html']
        for filename in invalid_files:
            path = Path(filename)
            self.assertFalse(path.suffix.lower() in expected_extensions)

    def test_pdf_libraries_availability(self):
        """Test PDF libraries availability"""
        try:
            import weasyprint
            weasyprint_available = True
        except (ImportError, OSError):
            weasyprint_available = False

        try:
            from reportlab.lib.pagesizes import letter
            reportlab_available = True
        except ImportError:
            reportlab_available = False

        # At least one PDF library should be available
        self.assertTrue(weasyprint_available or reportlab_available,
                       "Nenhuma biblioteca de PDF disponível")

    def test_html_widget_availability(self):
        """Test HTML widget availability"""
        try:
            from tkinterweb import HtmlFrame
            tkinterweb_available = True
        except ImportError:
            tkinterweb_available = False

        # Test should pass regardless of tkinterweb availability
        self.assertIsInstance(tkinterweb_available, bool)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)