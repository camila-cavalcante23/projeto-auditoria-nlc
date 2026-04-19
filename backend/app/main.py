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
    # Valida se o arquivo é um Zip
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .zip")

    audit = AuditService()
    resultados_finais = []

    try:
        content = await file.read()
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            # Detecta arquivos no ZIP 
            arquivos = [f for f in z.namelist() if not f.endswith('/')]
            
            print(f"--- Iniciando processamento de {len(arquivos)} arquivos ---")
            
            for index, nome_arquivo in enumerate(arquivos):
                conteudo_binario = z.read(nome_arquivo)
                
                
                texto, erro = ler_texto_seguro(conteudo_binario)
                
                if erro: 
                    print(f"Erro em {nome_arquivo}: {erro}")
                    continue

               
                print(f"Processando {nome_arquivo}... (Aguardando janela de cota)")
                time.sleep(15) 
            
               
                dados_extraidos = extrair_dados_com_ia(texto)
                
                if dados_extraidos:
                    # Detecção de Anomalias 
                    anomalias = audit.detectar_anomalias(dados_extraidos, texto)
                    
                  
                    registro = {
                        **dados_extraidos, 
                        "arquivo": nome_arquivo, 
                        "anomalias": str(anomalias),
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    resultados_finais.append(registro)
                    print(f"✅ [{index+1}/{len(arquivos)}] Sucesso: {nome_arquivo}")
                else:
                    print(f"❌ Falha na IA para: {nome_arquivo}")

        # Geração de CSV
        csv_data = gerar_csv_resultados(resultados_finais)
        
        return {
            "mensagem": "Processamento concluído",
            "total": len(resultados_finais),
            "resultados": resultados_finais,
            "csv_preview": csv_data[:500]
        }

    except Exception as e:
       
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail="Erro interno")