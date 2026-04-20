import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extrair_dados_com_ia(texto_documento):
    model = genai.GenerativeModel("gemini-1.5-flash-8b")

    try:
        response = model.generate_content(
            f"Extraia os dados desta nota em JSON: {texto_documento}",
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        print(f"IA Indisponível (Cota). Usando Extração de Contingência...")
        
        #CONTINGÊNCIA
        linhas = texto_documento.split('\n')
        dados_brutos = {}
        for linha in linhas:
            if ':' in linha:
                chave, valor = linha.split(':', 1)
                dados_brutos[chave.strip()] = valor.strip()
        
        return {
            "TIPO_DOCUMENTO": dados_brutos.get("TIPO_DOCUMENTO", "NOTA_FISCAL"),
            "NUMERO_DOCUMENTO": dados_brutos.get("NUMERO_DOCUMENTO", "EXTRAÇÃO_MANUAL"),
            "DATA_EMISSAO": dados_brutos.get("DATA_EMISSAO", "01/01/2026"),
            "FORNECEDOR": dados_brutos.get("FORNECEDOR", "Fornecedor não identificado"),
            "CNPJ_FORNECEDOR": dados_brutos.get("CNPJ_FORNECEDOR", "00.000.000/0001-00"),
            "VALOR_BRUTO": dados_brutos.get("VALOR_BRUTO", "R$ 0,00"),
            "DATA_PAGAMENTO": dados_brutos.get("DATA_PAGAMENTO", "01/01/2026"),
            "APROVADO_POR": dados_brutos.get("APROVADO_POR", "REVISÃO MANUAL"),
            "STATUS": dados_brutos.get("STATUS", "PENDENTE"),
            "HASH_VERIFICACAO": dados_brutos.get("HASH_VERIFICACAO", "N/A")
        }