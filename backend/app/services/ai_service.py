import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extrair_dados_com_ia(texto_documento):
    tentativas = 3

    for tentativa in range(tentativas):
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "system",
                        "content": "Responda APENAS com JSON válido. Não escreva nenhum texto antes ou depois."
                    },
                    {
                        "role": "user",
                        "content": f"""
Extraia os dados desta nota fiscal e retorne no seguinte formato JSON:

{{
"TIPO_DOCUMENTO": "",
"NUMERO_DOCUMENTO": "",
"DATA_EMISSAO": "",
"FORNECEDOR": "",
"CNPJ_FORNECEDOR": "",
"VALOR_BRUTO": "",
"DATA_PAGAMENTO": "",
"APROVADO_POR": "",
"STATUS": "",
"HASH_VERIFICACAO": ""
}}

Texto:
{texto_documento}
"""
                    }
                ],
                temperature=0
            )

            conteudo = response.choices[0].message.content.strip()

            
            inicio = conteudo.find("{")
            fim = conteudo.rfind("}") + 1
            json_str = conteudo[inicio:fim]

            return json.loads(json_str)

        except Exception as e:
            print(f"Erro na IA (tentativa {tentativa+1}): {e}")
            time.sleep(2)

    print("IA Indisponível. Usando Extração de Contingência...")


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