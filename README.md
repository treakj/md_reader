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

### Método 1: Via Windows Explorer

1. Clique com o botão direito em qualquer arquivo `.md`
2. Selecione **"Abrir com"** → **"Escolher outro aplicativo"**
3. Clique em **"Mais aplicativos"** → **"Procurar outro aplicativo neste PC"**
4. Navegue até a pasta do projeto e selecione `leitor_md.pyw`
5. Marque **"Sempre usar este aplicativo para abrir arquivos .md"**
6. Clique em **"OK"**

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

1. **Abrir arquivo**: Use `Ctrl+O` ou clique em "Abrir Arquivo"
2. **Exportar PDF**: Use `Ctrl+E` ou clique em "Exportar PDF"
3. **Sair**: Use `Ctrl+Q` ou feche a janela

### Linha de comando

```bash
# Abrir um arquivo específico
python leitor_md.pyw caminho/para/arquivo.md

# Abrir o programa sem arquivo
python leitor_md.pyw
```

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

- `markdown==3.5.1` - Processamento de Markdown
- `weasyprint==60.2` - Geração de PDF
- `pygments==2.17.2` - Syntax highlighting
- `tkinterweb==3.24.7` - Widget HTML para Tkinter

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
