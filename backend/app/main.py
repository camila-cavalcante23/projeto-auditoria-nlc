from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import zipfile
import io
import time 

from app.services.ai_service import extrair_dados_com_ia
from app.services.audit_service import AuditService
from app.utils.extractors import ler_texto_seguro
from app.utils.exporters import gerar_csv_resultados

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

LIMITE_IA = 100 
PROMPT_VERSION = "v1.0" 

@app.post("/processar")
async def processar_documentos(file: UploadFile = File(...)):
    audit = AuditService()
    resultados_finais = []
    arquivos_para_processar = [] 
    contador_ia = 0  

    try:
        content = await file.read()

        # Segurança 
        if not file.filename.endswith(('.zip', '.txt')):
            raise HTTPException(status_code=400, detail="Formato não suportado")

        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="Arquivo muito grande")

        # CASO 1: ZIP
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                for nome in z.namelist():
                    if not nome.endswith('/'):
                        arquivos_para_processar.append((nome, z.read(nome)))

        # CASO 2: TXT
        elif file.filename.endswith('.txt'):
            arquivos_para_processar.append((file.filename, content))

        print(f"--- Iniciando processamento de {len(arquivos_para_processar)} arquivo(s) ---")

        for index, (nome_arquivo, conteudo_binario) in enumerate(arquivos_para_processar):
            
            texto, erro = ler_texto_seguro(conteudo_binario)
            
            # ERRO DE ENCODING + ANOMALIA
            if erro: 
                print(f"Erro em {nome_arquivo}: {erro}")
                
                registro_erro = {
                    "arquivo": nome_arquivo,
                    "erro": erro,
                    "status_processamento": "ERRO",
                    "anomalias": [{
                        "anomalia": "Arquivo não processável",
                        "confianca": "Médio",
                        "evidencia": erro
                    }],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "prompt_version": PROMPT_VERSION
                }

                resultados_finais.append(registro_erro)
                continue

            # IA ou fallback
            if contador_ia < LIMITE_IA:
                print(f"Usando IA para {nome_arquivo}")
                dados_extraidos = extrair_dados_com_ia(texto)
                contador_ia += 1
                origem = "IA"
            else:
                print(f"Usando fallback para {nome_arquivo}")
                dados_extraidos = extrair_dados_com_ia(texto)  
                origem = "FALLBACK"

            if dados_extraidos:
                anomalias = audit.detectar_anomalias(dados_extraidos, texto)

                score, nivel = audit.calcular_risco(anomalias)
                
                registro = {
                    **dados_extraidos,
                    "arquivo": nome_arquivo,
                    "origem_extracao": origem,
                    "anomalias": anomalias, 
                    "risco_score": score,
                    "nivel_risco": nivel,
                    "status_processamento": "SUCESSO",
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "prompt_version": PROMPT_VERSION  
                }

                resultados_finais.append(registro)
                print(f" [{index+1}/{len(arquivos_para_processar)}] Sucesso! | Risco: {nivel} ({score})")
            else:
                print(f"Falha na extração para: {nome_arquivo}")

        # CSV principal
        csv_data = gerar_csv_resultados(resultados_finais)

  
        log_auditoria = []

        for r in resultados_finais:
            if r.get("anomalias"):
                for a in r["anomalias"]:
                    log_auditoria.append({
                        "arquivo": r.get("arquivo"),
                        "timestamp": r.get("timestamp"),
                        "regra": a.get("anomalia"),
                        "evidencia": a.get("evidencia"),
                        "confianca": a.get("confianca"),
                        "prompt_version": r.get("prompt_version")
                    })

        return {
            "mensagem": "Processamento concluído",
            "total": len(resultados_finais),
            "ia_utilizada": contador_ia,
            "resultados": resultados_finais,
            "log_auditoria": log_auditoria,  
            "csv_preview": csv_data[:500]
        }

    except Exception as e:
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail="Erro interno no processamento")