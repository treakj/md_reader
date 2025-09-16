# 🪟 Configurar MD Reader como Programa Padrão no Windows

Este guia explica **passo a passo** como definir o MD Reader como programa padrão para arquivos Markdown no Windows.

## 🎯 Método Recomendado: Via Windows Explorer

### Passo 1: Localizar um arquivo .md
1. Abra o **Windows Explorer** (Win + E)
2. Navegue até onde você tem arquivos `.md` 
3. Se não tiver nenhum, você pode usar o `sample.md` que vem com o projeto

### Passo 2: Configurar associação
1. **Clique com o botão direito** no arquivo `.md`
2. Selecione **"Abrir com"** → **"Escolher outro aplicativo"**

   ![image](https://user-images.githubusercontent.com/placeholder/open-with.png)

3. Na janela que abrir:
   - Clique em **"Mais aplicativos"**
   - Role para baixo e clique em **"Procurar outro aplicativo neste PC"**

   ![image](https://user-images.githubusercontent.com/placeholder/more-apps.png)

### Passo 3: Selecionar o MD Reader
1. Navegue até a pasta onde você instalou o MD Reader
2. **RECOMENDADO**: Selecione o arquivo **`md_reader.bat`** ⭐
3. **Alternativa**: Se não funcionar, tente `leitor_md.pyw`
4. **Marque a caixa** "Sempre usar este aplicativo para abrir arquivos .md"
5. Clique em **"OK"**

> 💡 **Por quê .bat?** Arquivos `.bat` são mais confiáveis como programa padrão no Windows

   ![image](https://user-images.githubusercontent.com/placeholder/select-app.png)

### ✅ Teste
Agora, ao clicar duas vezes em qualquer arquivo `.md`, ele deve abrir automaticamente no MD Reader!

---

## 🛠️ Método Alternativo: Configurações do Windows

### Para Windows 10/11:

1. **Abra Configurações**: Win + I
2. Vá para **"Aplicativos"** → **"Aplicativos padrão"**
3. Clique em **"Escolher aplicativos padrão por tipo de arquivo"**
4. **Procure por `.md`** na lista (use Ctrl+F para pesquisar)
5. Clique no ícone ao lado de `.md` 
6. Selecione **"Procurar um aplicativo"**
7. Navegue até `leitor_md.pyw` e selecione

   ![image](https://user-images.githubusercontent.com/placeholder/default-apps.png)

---

## 🔧 Método Avançado: Editor de Registro

> ⚠️ **CUIDADO**: Só use este método se você entende do Registry do Windows!

### Criar arquivo .reg automatizado:

1. Crie um arquivo chamado `setup_md_reader.reg`
2. Cole o conteúdo abaixo, **substituindo os caminhos**:

```reg
Windows Registry Editor Version 5.00

[HKEY_CLASSES_ROOT\.md]
@="MDReaderFile"

[HKEY_CLASSES_ROOT\.markdown]
@="MDReaderFile"

[HKEY_CLASSES_ROOT\MDReaderFile]
@="Markdown Document"
"FriendlyTypeName"="Arquivo Markdown"

[HKEY_CLASSES_ROOT\MDReaderFile\DefaultIcon]
@="C:\\CAMINHO\\PARA\\leitor_md.pyw,0"

[HKEY_CLASSES_ROOT\MDReaderFile\shell]
@="open"

[HKEY_CLASSES_ROOT\MDReaderFile\shell\open]
@="Abrir com MD Reader"

[HKEY_CLASSES_ROOT\MDReaderFile\shell\open\command]
@="\"C:\\Python\\python.exe\" \"C:\\CAMINHO\\PARA\\leitor_md.pyw\" \"%1\""
```

3. **Substitua** os caminhos:
   - `C:\\CAMINHO\\PARA\\leitor_md.pyw` → Caminho real do arquivo
   - `C:\\Python\\python.exe` → Caminho do seu Python

4. Execute o arquivo `.reg` como **administrador**

---

## 📝 Verificação e Teste

### Como saber se funcionou:

1. **Ícone mudou**: Arquivos `.md` devem mostrar um ícone diferente
2. **Abertura automática**: Clique duplo abre no MD Reader
3. **Menu de contexto**: "Abrir com" mostra MD Reader como padrão

### Se não funcionou:

1. ✅ **Verifique o caminho**: Certifique-se que `leitor_md.pyw` está no local correto
2. ✅ **Teste o programa**: Execute `python leitor_md.pyw` manualmente (não apenas `leitor_md.pyw`)
3. ✅ **Dependências**: Verifique se `pip install -r requirements.txt` foi executado
4. ✅ **Permissions**: Tente executar como administrador

### ⚠️ **IMPORTANTE - Sobre arquivos .pyw**:

O arquivo `.pyw` **NÃO PODE** ser executado diretamente no terminal:

```bash
# ❌ ERRADO - Não funciona
leitor_md.pyw
./leitor_md.pyw

# ✅ CORRETO - Use python antes
python leitor_md.pyw
python leitor_md.pyw arquivo.md
```

**Por quê?** Arquivos `.pyw` são "Python Windowed" e precisam do interpretador Python para executar. Eles são diferentes de executáveis `.exe`.

---

## 🚨 Problemas Comuns

### "Python não encontrado"
**Solução**: Use o caminho completo do Python no registro:
```
"C:\\Users\\SEU_USUARIO\\AppData\\Local\\Programs\\Python\\Python3X\\python.exe"
```

### "Arquivo não encontrado"
**Solução**: Verifique se todos os arquivos estão na mesma pasta:
- ✅ `leitor_md.pyw`
- ✅ `markdown_reader.py` 
- ✅ `requirements.txt`

### "Interface não abre"
**Solução**: 
1. Teste primeiro via terminal: `python leitor_md.pyw`
2. Verifique se há erros de dependências
3. Use o método 1 (Windows Explorer) que é mais confiável

---

## 💡 Dicas Extras

### Para múltiplos formatos:
Repita o processo para:
- `.markdown`
- `.mdown` 
- `.mkd`
- `.mkdn`

### Para remover a associação:
1. Clique direito no arquivo `.md`
2. "Abrir com" → "Escolher outro aplicativo"
3. Selecione outro programa (ex: Notepad)
4. Marque "Sempre usar..."

### Para criar atalho na área de trabalho:
1. Clique direito na área de trabalho
2. "Novo" → "Atalho"
3. Digite: `python "C:\CAMINHO\PARA\leitor_md.pyw"`
4. Nomeie como "MD Reader"

---

**🎉 Pronto! Agora você pode abrir arquivos Markdown diretamente no MD Reader!**
