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

@app.post("/processar")
async def processar_documentos(file: UploadFile = File(...)):
    audit = AuditService()
    resultados_finais = []
    arquivos_para_processar = [] 

    try:
        content = await file.read()

        # CASO 1: É um arquivo ZIP
        if file.filename.endswith('.zip'):
            with zipfile.ZipFile(io.BytesIO(content)) as z:
                for nome in z.namelist():
                    if not nome.endswith('/'):
                        arquivos_para_processar.append((nome, z.read(nome)))

        # CASO 2: É um arquivo TXT individual
        elif file.filename.endswith('.txt'):
            arquivos_para_processar.append((file.filename, content))
        
        else:
            raise HTTPException(status_code=400, detail="Formato não suportado. Envie .zip ou .txt")

        print(f"--- Iniciando processamento de {len(arquivos_para_processar)} arquivo(s) ---")
        
        for index, (nome_arquivo, conteudo_binario) in enumerate(arquivos_para_processar):
            texto, erro = ler_texto_seguro(conteudo_binario)
            
            if erro: 
                print(f"Erro em {nome_arquivo}: {erro}")
                continue

            # Se for mais de um arquivo,  um tempo maior para a IA não bloquear
            if len(arquivos_para_processar) > 1:
                print(f"Aguardando janela de cota para {nome_arquivo}...")
                time.sleep(15) 
            
            print(f"Enviando {nome_arquivo} para a IA...")
            dados_extraidos = extrair_dados_com_ia(texto)
            
            if dados_extraidos:
                anomalias = audit.detectar_anomalias(dados_extraidos, texto)
                
                registro = {
                    **dados_extraidos, 
                    "arquivo": nome_arquivo, 
                    "anomalias": str(anomalias),
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                resultados_finais.append(registro)
                print(f" [{index+1}/{len(arquivos_para_processar)}] Sucesso!")
            else:
                print(f"Falha na IA para: {nome_arquivo}")

        csv_data = gerar_csv_resultados(resultados_finais)
        
        return {
            "mensagem": "Processamento concluído",
            "total": len(resultados_finais),
            "resultados": resultados_finais,
            "csv_preview": csv_data[:500]
        }

    except Exception as e:
        print(f"Erro no servidor: {e}")
        raise HTTPException(status_code=500, detail=str(e))