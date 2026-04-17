import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

#Configura a API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERRO CRÍTICO: GEMINI_API_KEY não encontrada!")
else:
    genai.configure(api_key=api_key)
    #diagnóstico
    print("--- Modelos Disponíveis ---")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"-> {m.name}")
    except Exception:
        pass 
    print("---------------------------------------")

def extrair_dados_com_ia(texto_documento, retries=3):
    """
    Extrai dados usando IA com lógica de re-tentativa para evitar erros de cota (429).
    """
    # modelo que apareceu na lista
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"""
    Atue como um auditor financeiro rigoroso. Extraia os dados do documento abaixo.
    
    Regras Críticas:
    1. Retorne APENAS um objeto JSON válido.
    2. Se não conseguir extrair um campo, registre 'não extraído'.
    
    Campos: TIPO_DOCUMENTO, NUMERO_DOCUMENTO, DATA_EMISSAO, FORNECEDOR, 
    CNPJ_FORNECEDOR, VALOR_BRUTO, DATA_PAGAMENTO, APROVADO_POR, STATUS, HASH_VERIFICACAO.

    Texto:
    {texto_documento}
    """

    for i in range(retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            return json.loads(response.text)
            
        except Exception as e:
            # Se o erro for de cota (429)
            if "429" in str(e):
                espera = (i + 1) * 6 
                print(f"Cota atingida. Aguardando {espera}s para tentar novamente...")
                time.sleep(espera)
                continue
            
            print(f" Erro na extração: {e}")
            return None
            
    return None