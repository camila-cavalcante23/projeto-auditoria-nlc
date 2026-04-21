from datetime import datetime
import re

class AuditService:
    def __init__(self):
       
        self.nfs_processadas = set() 
        self.fornecedores_vistos = set()
        self.aprovadores_conhecidos = ["Maria Silva", "João Pereira", "Ana Costa"] 
        self.cnpj_por_fornecedor = {}
        self.valores_por_fornecedor = {}

    def limpar_valor(self, valor_str):
        """Remove R$ e converte string para float para cálculos."""
        if valor_str == "não extraído": 
            return 0.0
        try:
            limpo = re.sub(r'[^\d,]', '', valor_str).replace(',', '.')
            return float(limpo)
        except:
            return 0.0

    def detectar_anomalias(self, dados, texto_bruto):
        flags = []
        
        # 1. NF Duplicada
        id_unico = f"{dados['NUMERO_DOCUMENTO']}-{dados['CNPJ_FORNECEDOR']}"
        if id_unico in self.nfs_processadas:
            flags.append({
                "anomalia": "NF duplicada",
                "confianca": "Alto",
                "evidencia": dados['NUMERO_DOCUMENTO']
            })
        self.nfs_processadas.add(id_unico)

        # 2. NF emitida após pagamento
        try:
            if dados['DATA_EMISSAO'] != "não extraído" and dados['DATA_PAGAMENTO'] != "não extraído":
                dt_emissao = datetime.strptime(dados['DATA_EMISSAO'], '%d/%m/%Y')
                dt_pagamento = datetime.strptime(dados['DATA_PAGAMENTO'], '%d/%m/%Y')
                if dt_emissao > dt_pagamento:
                    flags.append({
                        "anomalia": "NF emitida após pagamento",
                        "confianca": "Alto",
                        "evidencia": f"Emissão: {dados['DATA_EMISSAO']}"
                    })
        except:
            pass 

        # 3. Fornecedor sem histórico
        if dados['FORNECEDOR'] not in self.fornecedores_vistos and dados['FORNECEDOR'] != "não extraído":
            flags.append({
                "anomalia": "Fornecedor sem histórico",
                "confianca": "Alto",
                "evidencia": dados['FORNECEDOR']
            })
        self.fornecedores_vistos.add(dados['FORNECEDOR'])

        # 4. STATUS inconsistente
        if "CANCELADO" in dados['STATUS'].upper() and dados['DATA_PAGAMENTO'] != "não extraído":
            flags.append({
                "anomalia": "STATUS inconsistente",
                "confianca": "Médio",
                "evidencia": "Cancelada mas paga"
            })

        # 5. Aprovador não reconhecido
        if dados['APROVADO_POR'] not in self.aprovadores_conhecidos and dados['APROVADO_POR'] != "não extraído":
            flags.append({
                "anomalia": "Aprovador não reconhecido",
                "confianca": "Médio",
                "evidencia": dados['APROVADO_POR']
            })

        # 6. CNPJ divergente
        if dados['FORNECEDOR'] != "não extraído" and dados['CNPJ_FORNECEDOR'] != "não extraído":
            cnpj_existente = self.cnpj_por_fornecedor.get(dados['FORNECEDOR'])
            
            if cnpj_existente and cnpj_existente != dados['CNPJ_FORNECEDOR']:
                flags.append({
                    "anomalia": "CNPJ divergente",
                    "confianca": "Alto",
                    "evidencia": dados['CNPJ_FORNECEDOR']
                })
            
            self.cnpj_por_fornecedor[dados['FORNECEDOR']] = dados['CNPJ_FORNECEDOR']

        # 7. Valor fora da faixa
        valor = self.limpar_valor(dados['VALOR_BRUTO'])

        if dados['FORNECEDOR'] != "não extraído" and valor > 0:
            lista = self.valores_por_fornecedor.setdefault(dados['FORNECEDOR'], [])
            
            if len(lista) >= 3:
                media = sum(lista) / len(lista)
                
                if valor > media * 2:
                    flags.append({
                        "anomalia": "Valor fora da faixa",
                        "confianca": "Médio",
                        "evidencia": f"Valor: {valor} > média: {round(media, 2)}"
                    })
            
            lista.append(valor)

        return flags
    

    # NOVO: CÁLCULO DE RISCO
    def calcular_risco(self, flags):
        score = 0

        for f in flags:
            confianca = f.get("confianca", "")

            if confianca == "Alto":
                score += 40
            elif confianca == "Médio":
                score += 20
            else:
                score += 10

        if score >= 70:
            nivel = "ALTO"
        elif score >= 30:
            nivel = "MÉDIO"
        else:
            nivel = "BAIXO"

        return score, nivel