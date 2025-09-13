# 🚀 Instalação Rápida - MD Reader

## 📦 Instalação via Git

```bash
# Clonar repositório
git clone https://github.com/treakj/md_reader.git
cd md_reader

# Instalar dependências
pip install -r requirements.txt

# Testar aplicação
python leitor_md.pyw
```

## ⚡ Instalação Manual

1. **Download**: Baixe o [ZIP do projeto](https://github.com/treakj/md_reader/archive/main.zip)
2. **Extrair**: Descompacte em uma pasta de sua escolha
3. **Dependências**: Execute `pip install -r requirements.txt`
4. **Executar**: Execute `python leitor_md.pyw`

## 🔧 Configurar como Programa Padrão

Após a instalação, consulte [WINDOWS_SETUP.md](WINDOWS_SETUP.md) para instruções detalhadas sobre como definir como programa padrão para arquivos .md no Windows.

### Método Rápido:
1. Clique direito em um arquivo `.md`
2. "Abrir com" → "Escolher outro aplicativo" 
3. Navegue até `leitor_md.pyw`
4. Marque "Sempre usar este aplicativo"

## ✅ Verificar Instalação

```bash
# Testar com arquivo de exemplo
python leitor_md.pyw sample.md

# Testar exportação PDF (Ctrl+E)
# Testar abertura de arquivos (Ctrl+O)
```

## 🆘 Problemas?

- **"Módulo não encontrado"**: Execute `pip install -r requirements.txt`
- **"Python não encontrado"**: Certifique-se que Python está no PATH
- **Interface não abre**: Verifique se há arquivos faltando na pasta

Para mais detalhes, consulte o [README.md](README.md) completo.
