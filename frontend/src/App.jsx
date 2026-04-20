import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; 

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/processar', formData);
      console.log("Dados que chegaram do Backend:", response.data);
      
      if (response.data && response.data.resultados) {
        setResults(response.data.resultados);
      } else {
        alert("O backend respondeu, mas a lista de resultados veio vazia.");
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

    // Atualizado com novos cabeçalhos para o BI
    const headers = "Arquivo;Fornecedor;CNPJ;Emissao;Valor;Aprovador;Status;Anomalias\n";
    
    const rows = results.map(res => {
      const status = res.anomalias === "[]" ? "Limpo" : "Atenção";
      return `${res.arquivo};${res.FORNECEDOR};${res.CNPJ_FORNECEDOR};${res.DATA_EMISSAO};${res.VALOR_BRUTO};${res.APROVADO_POR};${status};${res.anomalias.replace(/;/g, ',')}`;
    }).join("\n");

    const blob = new Blob(["\ufeff" + headers + rows], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", "auditoria_nlconsulting.csv");
    link.click();
  };

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
        
        <button 
          className="btn-audit" 
          onClick={handleUpload} 
          disabled={loading || !file}
        >
          {loading ? "Processando motor de IA..." : "Iniciar Auditoria"}
        </button>
      </div>

      {results.length > 0 && (
        <div className="results-container">
          <div className="results-header">
            <div>
              <h2>Relatório de Auditoria</h2>
              <p className="subtitle">{results.length} documentos analisados pelo sistema híbrido</p>
            </div>
            <button className="btn-export-premium" onClick={exportToCSV}>
              <span>📥</span> Exportar para Power BI
            </button>
          </div>

          <div className="table-responsive">
            <table className="audit-table">
              <thead>
                <tr>
                  <th>Arquivo</th>
                  <th>Fornecedor / CNPJ</th>
                  <th>Emissão</th>
                  <th>Valor Bruto</th>
                  <th>Aprovador</th>
                  <th>Status de Risco</th>
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
                    <td>👤 {res.APROVADO_POR}</td>
                   <td title={res.anomalias !== "[]" ? res.anomalias : "Nenhuma anomalia detectada"}>
                 {res.anomalias === "[]" ? (
                 <span className="status-badge limpo">✔️ Limpo</span>
                      ) : (
                   <div className="status-container">
                   <span className="status-badge atencao">⚠️ Atenção</span>
       
                  <p className="anomaly-text">{res.anomalias.replace(/[\[\]']/g, '')}</p>
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