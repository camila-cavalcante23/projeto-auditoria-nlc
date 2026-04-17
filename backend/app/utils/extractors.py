import chardet

def ler_texto_seguro(conteudo_binario):
    """Detecta o encoding e lê o arquivo sem quebrar[cite: 32, 43]."""
    if not conteudo_binario:
        return None, "Arquivo vazio"


    resultado = chardet.detect(conteudo_binario)
    encoding = resultado['encoding']

    try:
        texto = conteudo_binario.decode(encoding or 'utf-8')
        return texto, None
    except Exception:
        return None, f"Falha no encoding ({encoding})"