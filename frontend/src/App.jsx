import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [logAuditoria, setLogAuditoria] = useState([]); 

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/processar', formData);

      if (response.data) {
        setResults(response.data.resultados || []);
        setLogAuditoria(response.data.log_auditoria || []); 
      } else {
        alert("Resposta inválida do backend.");
      }

    } catch (error) {
      alert("Erro ao conectar com o backend.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  
  const exportToCSV = () => {
    if (results.length === 0) return;

    const headers = "Arquivo;Fornecedor;CNPJ;Emissao;Valor;Aprovador;Score_Risco;Nivel_Risco;Anomalias\n";
    
    const rows = results.map(res => {
      const anomaliasTexto = (res.anomalias || []).map(a => a.anomalia).join(" | ");

      return `${res.arquivo};${res.FORNECEDOR};${res.CNPJ_FORNECEDOR};${res.DATA_EMISSAO};${res.VALOR_BRUTO};${res.APROVADO_POR};${res.risco_score};${res.nivel_risco};${anomaliasTexto}`;
    }).join("\n");

    const blob = new Blob(["\ufeff" + headers + rows], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "auditoria_nlconsulting.csv");
    link.click();
  };

  
  const exportLogCSV = () => {
    if (logAuditoria.length === 0) return;

    const headers = "Arquivo;Timestamp;Regra;Evidencia;Confianca;Prompt_Version\n";

    const rows = logAuditoria.map(l =>
      `${l.arquivo};${l.timestamp};${l.regra};${l.evidencia};${l.confianca};${l.prompt_version}`
    ).join("\n");

    const blob = new Blob(["\ufeff" + headers + rows], { type: 'text/csv;charset=utf-8;' });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "log_auditoria.csv");
    link.click();
  };

 
  const totalAlto = results.filter(r => r.nivel_risco?.toLowerCase() === 'alto').length;
  const totalMedio = results.filter(r => r.nivel_risco?.toLowerCase() === 'medio').length;
  const totalBaixo = results.filter(r => r.nivel_risco?.toLowerCase() === 'baixo').length;

  return (
    <div className="main-container">

      <header className="app-header">
        <div className="brand-section">
          <h1>Auditoria IA</h1>
          <p>NLConsulting Document Analyzer</p>
        </div>
        <div className="slogan-section">
          <p>Sua auditoria, mais simples.</p>
        </div>
      </header>

      <div className="upload-card">
        <label className="drop-zone">
          <input 
            type="file" 
            style={{ display: 'none' }} 
            onChange={(e) => setFile(e.target.files[0])} 
            accept=".zip,.txt"
          />
          <div className="upload-icon">☁️</div>
          <p className="file-name">
            {file ? file.name : "Clique para selecionar arquivo .zip ou .txt"}
          </p>
        </label>
        
        <button className="btn-audit" onClick={handleUpload} disabled={loading || !file}>
          {loading ? "Processando motor de IA..." : "Iniciar Auditoria"}
        </button>
      </div>

      {loading && <p className="loading-text">🔄 Processando documentos...</p>}

      {results.length > 0 && (
        <div>

          <div className="results-header">
            <div>
              <h2>Relatório Inteligente de Auditoria</h2>
              <p className="subtitle">
                {results.length} documentos analisados
              </p>

              <p>
                🔴 Alto: {totalAlto} | 🟡 Médio: {totalMedio} | 🟢 Baixo: {totalBaixo}
              </p>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button className="btn-export-premium" onClick={exportToCSV}>
                📥 Exportar CSV
              </button>

              <button className="btn-export-premium" onClick={exportLogCSV}>
                📄 Log Auditoria
              </button>
            </div>
          </div>

          <div className="table-responsive">
            <table className="audit-table">
              <thead>
                <tr>
                  <th>Arquivo</th>
                  <th>Fornecedor / CNPJ</th>
                  <th>Emissão</th>
                  <th>Valor Bruto</th>
                  <th>Risco</th>
                  <th>Status / Anomalias</th>
                </tr>
              </thead>

              <tbody>
                {results.map((res, i) => (
                  <tr key={i}>

                    <td>📄 {res.arquivo}</td>

                    <td>
                      <div className="vendor-info">
                        <span className="vendor-name">{res.FORNECEDOR}</span>
                        <span className="vendor-cnpj">{res.CNPJ_FORNECEDOR}</span>
                      </div>
                    </td>

                    <td>{res.DATA_EMISSAO}</td>

                    <td className="value-cell">{res.VALOR_BRUTO}</td>

                    <td>
                      <span className={`risk-badge ${res.nivel_risco?.toLowerCase()}`}>
                        {res.nivel_risco} ({res.risco_score})
                      </span>
                    </td>

                    <td>
                      {res.status_processamento === "ERRO" ? (
                        <div>
                          <span className="status-badge erro">❌ Erro</span>
                          <p>{res.erro}</p>
                        </div>
                      ) : (res.anomalias || []).length === 0 ? (
                        <span className="status-badge limpo">✔️ Limpo</span>
                      ) : (
                        <div className="status-container">
                          <span className="status-badge atencao">⚠️ Atenção</span>
                          <p className="anomaly-text">
                            {(res.anomalias || []).map((a, index) => (
                              <span key={index}>
                                • {a.anomalia}
                                <br />
                              </span>
                            ))}
                          </p>
                        </div>
                      )}
                    </td>

                  </tr>
                ))}
              </tbody>
            </table>
          </div>

        </div>
      )}
    </div>
  );
}

export default App;