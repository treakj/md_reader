# 📖 MD Reader - Leitor de Markdown

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey.svg" alt="Windows">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="MIT License">
  <img src="https://img.shields.io/badge/GUI-Tkinter-orange.svg" alt="Tkinter GUI">
</div>

<p align="center">
  <strong>Um leitor simples e elegante de arquivos Markdown com funcionalidade de exportação para PDF</strong>
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-instalação">Instalação</a> •
  <a href="#-como-usar">Como Usar</a> •
  <a href="#-programa-padrão">Programa Padrão</a> •
  <a href="#-contribuindo">Contribuindo</a>
</p>

## ✨ Funcionalidades

### 🔥 Novidades na Versão 2.0

- 🌙 **Modo Escuro**: Interface noturna confortável para os olhos
- 🔍 **Busca Avançada**: Encontre texto rapidamente com navegação entre resultados
- 🔎 **Controles de Zoom**: Aumente ou diminua o tamanho do texto (50% - 300%)
- 📚 **Arquivos Recentes**: Acesso rápido aos últimos documentos abertos
- 🎨 **Interface Aprimorada**: Design moderno com melhor usabilidade
- 📝 **Validação de Arquivos**: Verificação robusta de arquivos antes da abertura
- 📊 **Logging**: Sistema de log para diagnóstico de problemas
- 💾 **Configurações Persistentes**: Suas preferências são salvas automaticamente

### Funcionalidades Principais

- 📖 **Visualização de Markdown**: Renderização elegante de arquivos `.md` com syntax highlighting
- 📄 **Exportação PDF**: Converta seus documentos Markdown para PDF com formatação preservada
- 🎨 **Interface amigável**: Interface gráfica limpa e intuitiva
- ⚡ **Abertura rápida**: Pode ser definido como programa padrão para arquivos `.md`
- 🔧 **Suporte completo**: Tabelas, código, links, imagens e mais

## 🚀 Instalação

### 1. Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o programa

**Para desenvolvimento/debug (com console):**
```bash
python markdown_reader.py
```

**Para uso normal (sem console):**
```bash
python leitor_md.pyw
```

> ⚠️ **Importante**: O arquivo `.pyw` não pode ser executado diretamente no terminal (ex: `leitor_md.pyw`). Você deve usar `python leitor_md.pyw` ou clicar duas vezes no arquivo.

### 🤔 Diferença entre `.py` e `.pyw`:

| Extensão | Uso | Console | Melhor para |
|----------|-----|---------|-------------|
| `.py` | `python markdown_reader.py` | ✅ Visível | Debug, desenvolvimento |
| `.pyw` | `python leitor_md.pyw` | ❌ Oculto | Usuário final, programa padrão |

- **`.py`**: Mostra janela do console = melhor para debug
- **`.pyw`**: Sem console = interface mais limpa para usuários

## 🔧 Configurar como Programa Padrão (Windows)

Para definir o Leitor MD como programa padrão para arquivos `.md`:

### Método 1: Via Windows Explorer (Recomendado)

1. Clique com o botão direito em qualquer arquivo `.md`
2. Selecione **"Abrir com"** → **"Escolher outro aplicativo"**
3. Clique em **"Mais aplicativos"** → **"Procurar outro aplicativo neste PC"**
4. Navegue até a pasta do projeto e selecione **`md_reader.bat`** ⭐
5. Marque **"Sempre usar este aplicativo para abrir arquivos .md"**
6. Clique em **"OK"**

> 💡 **Por que `.bat` é melhor**: Arquivos `.bat` são mais confiáveis como programa padrão no Windows que arquivos `.pyw`

### Método 2: Via Configurações do Windows

1. Abra **Configurações** → **Aplicativos** → **Aplicativos padrão**
2. Clique em **"Escolher aplicativos padrão por tipo de arquivo"**
3. Procure por `.md` na lista
4. Clique no aplicativo atual ao lado de `.md`
5. Selecione **"Procurar um aplicativo na Microsoft Store"** ou **"Mais aplicativos"**
6. Navegue até `leitor_md.pyw` e selecione

### Método 3: Via Registro (Avançado)

Você pode criar um arquivo `.reg` para automatizar o processo:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.md]
@="MarkdownFile"

[HKEY_CLASSES_ROOT\MarkdownFile]
@="Markdown Document"

[HKEY_CLASSES_ROOT\MarkdownFile\shell\open\command]
@="\"C:\\Python\\python.exe\" \"C:\\caminho\\para\\leitor_md.pyw\" \"%1\""
```

> ⚠️ **Importante**: Substitua os caminhos pelos caminhos corretos do Python e do programa.

## 🎮 Como usar

### Interface Gráfica

#### 📁 Arquivo
- **Abrir arquivo**: `Ctrl+O` ou clique em "Abrir Arquivo"
- **Arquivos Recentes**: Acesso rápido aos últimos 20 documentos
- **Exportar PDF**: `Ctrl+E` ou clique em "Exportar PDF"
- **Sair**: `Ctrl+Q` ou feche a janela

#### 🔍 Visualizar
- **Buscar**: `Ctrl+F` - Busca de texto com navegação entre resultados
- **Modo Escuro**: Alternar entre tema claro e escuro
- **Zoom In**: `Ctrl++` - Aumentar tamanho do texto
- **Zoom Out**: `Ctrl+-` - Diminuir tamanho do texto
- **Zoom Normal**: `Ctrl+0` - Restaurar tamanho original

#### 🎛️ Barra de Ferramentas
- Botões rápidos para abrir arquivo e exportar PDF
- Controles de zoom com visualização da porcentagem
- Toggle de modo escuro
- Botão de busca rápida

### Linha de comando

**Usando Python diretamente:**
```bash
# Abrir um arquivo específico
python leitor_md.pyw caminho/para/arquivo.md

# Abrir o programa sem arquivo
python leitor_md.pyw
```

**Usando o arquivo batch (Windows):**
```bash
# Abrir um arquivo específico
md_reader.bat caminho/para/arquivo.md

# Abrir o programa sem arquivo
md_reader.bat
```

> 💡 **Dica**: O arquivo `md_reader.bat` é mais confiável para definir como programa padrão no Windows

## 📋 Formatos suportados

- `.md` - Markdown padrão
- `.markdown` - Markdown longo
- `.mdown` - Markdown alternativo
- `.mkd` - Markdown curto
- `.mkdn` - Markdown curto alternativo

## 🎨 Funcionalidades Markdown

O Leitor MD suporta:

- **Títulos** (`# ## ### ####`)
- **Texto em negrito** (`**texto**`)
- **Texto em itálico** (`*texto*`)
- **Código inline** (`código`)
- **Blocos de código** com syntax highlighting
- **Listas** numeradas e com marcadores
- **Links** e **imagens**
- **Tabelas**
- **Citações** (`> texto`)
- **Separadores** (`---`)

## 📦 Dependências

### Bibliotecas Principais
- `markdown==3.5.1` - Processamento de Markdown
- `weasyprint==59.0` - Geração de PDF de alta qualidade
- `reportlab==4.0.7` - Fallback para geração de PDF
- `pygments==2.17.2` - Syntax highlighting
- `tkinterweb==3.24.7` - Widget HTML para Tkinter

### Bibliotecas Padrão do Python
- `tkinter` - Interface gráfica (já inclusa no Python)
- `json` - Configurações e arquivos recentes
- `logging` - Sistema de logs
- `pathlib` - Manipulação de caminhos de arquivos
- `html.parser` - Parser HTML para PDF export
- `tempfile` - Arquivos temporários

### Sistema de Fallback
O aplicativo possui um sistema robusto de fallback:
- **PDF Export**: WeasyPrint → ReportLab → HTML (fallback)
- **HTML Rendering**: tkinterweb → Text widget (fallback)
- **File Validation**: Verificação completa antes da abertura

## 🧪 Testes

Execute a suíte de testes para verificar a funcionalidade:

```bash
python test_markdown_reader.py
```

Os testes cobrem:
- Validação de arquivos
- Carregamento de configurações
- Parsing de Markdown
- Extensões suportadas

## 🚀 Atualizações Recentes (v2.0.1)

### ✅ Bugs Corrigidos

- **🐛 Erro "margin not defined"**: Corrigido problema de f-string escaping em CSS que impedia abertura de arquivos
- **🌙 Modo Escuro**: Agora funciona corretamente, aplicando tema tanto na interface quanto no conteúdo do documento
- **🔍 Zoom**: Controles de zoom agora escalam o texto do documento corretamente (50% - 300%)
- **⚙️ Configuração HTML**: Removido erro de configuração inválida do HtmlFrame

### 📈 Melhorias

- **CSS Dinâmico**: Cores e tamanhos de fonte se ajustam automaticamente ao modo e zoom
- **Melhor Contraste**: Modo escuro com melhor legibilidade
- **Logs Aprimorados**: Mensagens de erro mais claras para diagnóstico

**Status**: ✅ **Todas as funcionalidades principais funcionando perfeitamente!**

## 🐛 Solução de problemas

### Erro: "Módulo não encontrado"

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install -r requirements.txt
```

### Erro de PDF: "weasyprint"

No Windows, pode ser necessário instalar dependências adicionais:

```bash
# Instalar GTK3 runtime (necessário para weasyprint)
# Baixe de: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
```

### Interface não carrega HTML

Se a biblioteca `tkinterweb` não estiver disponível, o programa usará um widget de texto simples como fallback.

### Logs de Erro

O aplicativo gera logs em `md_reader.log` para diagnóstico de problemas.

### Configurações

As configurações são salvas em `md_reader_config.json`:
- Modo escuro
- Nível de zoom
- Arquivos recentes
- Geometria da janela

## 🔄 Atualizações

Para atualizar as dependências:

```bash
pip install --upgrade -r requirements.txt
```

## 📝 Licença

Este projeto é de código aberto. Sinta-se livre para usar, modificar e distribuir.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se livre para:

- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 📞 Suporte

Se você encontrar algum problema ou tiver dúvidas, por favor:

1. Verifique se todas as dependências estão instaladas
2. Certifique-se de estar usando Python 3.8+
3. Verifique os logs de erro para mais detalhes

---

**Desenvolvido com ❤️ usando Python e Tkinter**
