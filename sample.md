# Exemplo de Documento Markdown

Este é um documento de exemplo para testar o **Leitor MD**.

## Funcionalidades Testadas

### Formatação Básica

- **Texto em negrito**
- *Texto em itálico*
- `Código inline`
- ~~Texto riscado~~

### Listas

#### Lista não numerada:
- Item 1
- Item 2
  - Subitem 2.1
  - Subitem 2.2
- Item 3

#### Lista numerada:
1. Primeiro item
2. Segundo item
3. Terceiro item

### Código

Aqui está um exemplo de código Python:

```python
def fibonacci(n):
    """Calcula a sequência de Fibonacci."""
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Testando a função
for i in range(10):
    print(f"F({i}) = {fibonacci(i)}")
```

### Tabela

| Nome | Idade | Cidade |
|------|-------|--------|
| João | 25    | São Paulo |
| Maria | 30    | Rio de Janeiro |
| Pedro | 35    | Belo Horizonte |

### Citações

> "A programação é uma arte, e como toda arte, requer prática e paixão."
> 
> — Programador Anônimo

### Links e Imagens

- [Google](https://www.google.com)
- [GitHub](https://www.github.com)

### Separador

---

## Conclusão

Este documento testa as principais funcionalidades de renderização do Markdown:

1. ✅ Títulos e subtítulos
2. ✅ Formatação de texto
3. ✅ Listas
4. ✅ Blocos de código com syntax highlighting
5. ✅ Tabelas
6. ✅ Citações
7. ✅ Links
8. ✅ Separadores

**Teste concluído com sucesso!** 🎉
