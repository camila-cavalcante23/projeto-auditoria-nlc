import os
import json
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

CAMPOS_PADRAO = [
    "TIPO_DOCUMENTO",
    "NUMERO_DOCUMENTO",
    "DATA_EMISSAO",
    "FORNECEDOR",
    "CNPJ_FORNECEDOR",
    "VALOR_BRUTO",
    "DATA_PAGAMENTO", 
    "APROVADO_POR",
    "STATUS",
    "HASH_VERIFICACAO"
]


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
Extraia os dados desta nota fiscal e retorne no seguinte formato JSON.

Se algum campo não estiver presente, retorne exatamente: "não extraído".

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

            # Extrair JSON 
            inicio = conteudo.find("{")
            fim = conteudo.rfind("}") + 1
            json_str = conteudo[inicio:fim]

            dados = json.loads(json_str)

            # GARANTIR TODOS OS CAMPOS
            for campo in CAMPOS_PADRAO:
                if campo not in dados or not dados[campo]:
                    dados[campo] = "não extraído"

            return dados

        except Exception as e:
            print(f"Erro na IA (tentativa {tentativa+1}): {e}")
            time.sleep(2)

    print("IA Indisponível. Usando Extração de Contingência...")

    # FALLBACK 
    linhas = texto_documento.split('\n')
    dados_brutos = {}

    for linha in linhas:
        if ':' in linha:
            chave, valor = linha.split(':', 1)
            dados_brutos[chave.strip()] = valor.strip()

    # RETORNO PADRÃO COM "não extraído"
    return {
        campo: dados_brutos.get(campo, "não extraído")
        for campo in CAMPOS_PADRAO
    }