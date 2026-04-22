# 🧠 Auditor de Documentos com IA — NLConsulting

Aplicação web full stack para processamento automatizado de documentos financeiros utilizando Inteligência Artificial (LLaMA 3.1), com foco em extração de dados, detecção de anomalias e visualização em Business Intelligence.

🚀 **(Frontend):** [https://projeto-auditoria-nlc.vercel.app/](https://projeto-auditoria-nlc.vercel.app/)

⚙️ **API (Backend):** [https://projeto-auditoria-nlc.onrender.com](https://projeto-auditoria-nlc.onrender.com)

📖Documentação Swagger: [https://projeto-auditoria-nlc.onrender.com/docs](https://projeto-auditoria-nlc.onrender.com/docs). 

---

## 📌 Sobre o Projeto
Este projeto foi desenvolvido para o desafio técnico da **NLConsulting (2026)**. A ferramenta simula um cenário real de auditoria, processando lotes de até 1.000 documentos para identificar fraudes, erros de preenchimento e inconsistências operacionais de forma automatizada.

## ⚙️ Funcionalidades
* **Upload em Lote:** Suporte a arquivos `.zip` contendo centenas de faturas ou múltiplos arquivos `.txt`.
* **Extração via IA (LLaMA 3.1):** Utilização do modelo LLaMA 3.1 via Groq API para extração estruturada de dados não estruturados.
* **Motor de Auditoria:** Identificação automática de 8 tipos de anomalias com classificação de risco (Baixo, Médio, Alto).
* **Dashboard BI:** Integração com Power BI para análise macro de riscos e performance de fornecedores.
* **Rastreabilidade (Audit Trail):** Logs detalhados contendo versão do prompt, timestamp e evidências para cada decisão da IA.

## 🛠️ Tecnologias Utilizadas
* **Frontend:** React.js, Axios, Vite.
* **Backend:** Python 3.11, FastAPI, Uvicorn.
* **IA:** Groq Cloud (LLaMA 3.1 70B).
* **BI:** Power BI Desktop (análise de dados via CSV).
* **Infraestrutura:** Vercel (Frontend) e Render (Backend/API).

## 📊 Business Intelligence
O projeto inclui um dashboard interativo (localizado na pasta `/dashboard`) que permite:
* Visualizar o percentual de documentos por nível de risco.
* Filtrar inconsistências por fornecedor específico.
* Analisar as regras de auditoria mais infringidas.

## 🔍 Regras de Auditoria Implementadas
A aplicação valida padrões críticos conforme o briefing:
* 🔴 **Duplicidade:** Checagem de número da NF por fornecedor.
* 🔴 **Divergência de CNPJ:** Validação de cadastro.
* 🔴 **Inconsistência Cronológica:** NF emitida após a data de pagamento.
* 🟡 **Anomalia de Valor:** Desvio em relação à média histórica do fornecedor.
* 🟡 **Aprovador Inválido:** Verificação contra lista de usuários autorizados.

## 🔐 Segurança
* **Variáveis de Ambiente:** Gestão segura de chaves de API no Render e Vercel.
* **CORS:** Configuração de políticas de acesso entre domínios.
* **Versionamento de Prompt:** Garantia de que a lógica de extração pode ser auditada e evoluída.

## ▶️ Como Executar Localmente
1. **Clone o repositório:**
   git clone [https://github.com/camila-cavalcante23/projeto-auditoria-nlc.git](https://github.com/camila-cavalcante23/projeto-auditoria-nlc.git)


## 2. Backend e Frontend

Para executar o projeto, vá até a pasta `/backend` e instale as dependências com `pip install -r requirements.txt`. Em seguida, configure a variável de ambiente `GROQ_API_KEY` no arquivo `.env` e execute o servidor com `uvicorn app.main:app --reload`. 

Depois, acesse a pasta `/frontend`, instale as dependências com `npm install` e inicie a aplicação utilizando `npm run dev`.

---

## 👩‍💻 Autor

**Camila Paiva**  
Software Developer
