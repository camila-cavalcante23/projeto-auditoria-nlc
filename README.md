# 🧠 Auditor de Documentos com IA — NLConsulting



Aplicação web full stack para processamento automatizado de documentos financeiros utilizando Inteligência Artificial, com foco em extração de dados, detecção de anomalias e geração de relatórios auditáveis.



🚀 **** | 📊 ****



## 📌 Sobre o Projeto

Este projeto foi desenvolvido para o desafio técnico da **NLConsulting (2026)**.A ferramenta simula um cenário real de auditoria, processando até 1.000 documentos para identificar fraudes e inconsistências operacionais.



## ⚙️ Funcionalidades

* **Upload Inteligente:** Aceita arquivos `.zip` ou múltiplos `.txt`.

* **Extração Híbrida (IA + Fallback):** Processamento via **LLaMA 3.1** com motor de contingência (Regex) para garantir 100% de disponibilidade mesmo sob Rate Limit da API.

* **Auditoria de Riscos:** Identificação automática de 8 tipos de anomalias com classificação de risco (Baixo, Médio, Alto)

* **Log de Auditoria:** Registro rastreável com timestamp, regra disparada, evidência e versão do prompt.

* **Exportação:** Geração de CSV para alimentação direta de dashboards de BI.



## 🛠️ Tecnologias Utilizadas

* **Frontend:** React, Axios, CSS3.

* **Backend:** Python, FastAPI, Groq API (LLaMA 3.1).

* **Dados:** Power BI, CSV.



## 🔍 Anomalias Detectadas

A aplicação identifica padrões críticos conforme os requisitos do briefing:

* 🔴 **NF duplicada:** Checagem de número + fornecedor.

* 🔴 **CNPJ divergente:** Validação contra o padrão do fornecedor identificado.

* 🔴 **NF emitida após pagamento:** Inconsistência cronológica de datas.

* 🟡 **Valor fora da faixa:** Desvio estatístico em relação à média do fornecedor.

* 🟡 **Aprovador não reconhecido:** Verificação contra lista de aprovadores permitidos.



## 🔐 Segurança e Rastreabilidade

* **Proteção de Credenciais:** Chaves de API gerenciadas via variáveis de ambiente (`.env`)

* **Sanitização:** Validação de tipo e tamanho de arquivo antes do processamento.

* **Audit Trail:** Histórico completo de decisões da IA para cada documento.

## ▶️ Como Executar Localmente

### 1. Clone o repositório

git clone https://github.com/camila-cavalcante23/projeto-auditoria-nlc.git
cd projeto-auditoria-nlc


2. No `/backend`, instale as dependências (`pip install -r requirements.txt`) Crie o arquivo .env  e configure a `GROQ_API_KEY` 
3. Execute: `uvicorn app.main:app --reload`.
4. No `/frontend`, execute `npm install` e `npm run dev`.

## 👩‍💻 Autor
**Camila Paiva**
*Software Developer*
