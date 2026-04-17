import pandas as pd
import io

def gerar_csv_resultados(lista_resultados):
    """Converte os dados processados em CSV para o Power BI[cite: 40, 65]."""
    df = pd.DataFrame(lista_resultados)
    
   
    output = io.StringIO()
    df.to_csv(output, index=False, encoding='utf-8-sig', sep=';')
    return output.getvalue()