from datetime import datetime
import re

class AuditService:
    def __init__(self):
        # Memória temporária para detectar duplicatas e novos fornecedores 
        self.nfs_processadas = set() 
        self.fornecedores_vistos = set()
        self.aprovadores_conhecidos = ["Maria Silva", "João Pereira", "Ana Costa"] 

    def limpar_valor(self, valor_str):
        """Remove R$ e converte string para float para cálculos."""
        if valor_str == "não extraído": return 0.0
        try:
            # Remove símbolos e ajusta separadores decimais
            limpo = re.sub(r'[^\d,]', '', valor_str).replace(',', '.')
            return float(limpo)
        except:
            return 0.0

    def detectar_anomalias(self, dados, texto_bruto):
        """
        Aplica as regras de negócio do briefing.
        Retorna uma lista de flags de anomalia.
        """
        flags = []
        
        # 1. NF Duplicada (Mesmo número + Mesmo fornecedor) 
        id_unico = f"{dados['NUMERO_DOCUMENTO']}-{dados['CNPJ_FORNECEDOR']}"
        if id_unico in self.nfs_processadas:
            flags.append({"anomalia": "NF duplicada", "confianca": "Alto", "evidencia": dados['NUMERO_DOCUMENTO']})
        self.nfs_processadas.add(id_unico)

  
        try:
            if dados['DATA_EMISSAO'] != "não extraído" and dados['DATA_PAGAMENTO'] != "não extraído":
                dt_emissao = datetime.strptime(dados['DATA_EMISSAO'], '%d/%m/%Y')
                dt_pagamento = datetime.strptime(dados['DATA_PAGAMENTO'], '%d/%m/%Y')
                if dt_emissao > dt_pagamento:
                    flags.append({"anomalia": "NF emitida após pagamento", "confianca": "Alto", "evidencia": f"Emissão: {dados['DATA_EMISSAO']}"})
        except:
            pass 

    
        if dados['FORNECEDOR'] not in self.fornecedores_vistos and dados['FORNECEDOR'] != "não extraído":
            flags.append({"anomalia": "Fornecedor sem histórico", "confianca": "Alto", "evidencia": dados['FORNECEDOR']})
        self.fornecedores_vistos.add(dados['FORNECEDOR'])

      
        if "CANCELADO" in dados['STATUS'].upper() and dados['DATA_PAGAMENTO'] != "não extraído":
            flags.append({"anomalia": "STATUS inconsistente", "confianca": "Médio", "evidencia": "Cancelada mas paga"})

     
        if dados['APROVADO_POR'] not in self.aprovadores_conhecidos and dados['APROVADO_POR'] != "não extraído":
            flags.append({"anomalia": "Aprovador não reconhecido", "confianca": "Médio", "evidencia": dados['APROVADO_POR']})

        return flags