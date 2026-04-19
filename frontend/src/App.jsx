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

    
    const headers = "Arquivo;Fornecedor;Valor;CNPJ;Status;Anomalias\n";
    
    // Mapeia os resultados para o formato de linha 
    const rows = results.map(res => {
      const status = res.anomalias === "[]" ? "Limpo" : "Atenção";
      return `${res.arquivo};${res.FORNECEDOR};${res.VALOR_BRUTO};${res.CNPJ_FORNECEDOR};${status};${res.anomalias.replace(/;/g, ',')}`;
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
            accept=".zip"
          />
          <div className="upload-icon">☁️</div>
          <p className="file-name">
            {file ? file.name : "Clique para selecionar o arquivo .zip"}
          </p>
        </label>
        
        <button 
          className="btn-audit" 
          onClick={handleUpload} 
          disabled={loading || !file}
        >
          {loading ? "Processando..." : "Iniciar Auditoria"}
        </button>
      </div>

      {results.length > 0 && (
        <div className="results-container">
          <div className="results-actions">
            <h2>Resultados da Análise</h2>
            
            <button className="btn-export" onClick={exportToCSV}>
              Exportar para Power BI (CSV)
            </button>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Arquivo</th>
                  <th>Fornecedor</th>
                  <th>Valor</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {results.map((res, i) => (
                  <tr key={i}>
                    <td>📄 {res.arquivo}</td>
                    <td className="vendor-name">{res.FORNECEDOR}</td>
                    <td className="value-cell">{res.VALOR_BRUTO}</td>
                    <td>
                      {res.anomalias === "[]" ? (
                        <span className="status-badge limpo">✔️ Limpo</span>
                      ) : (
                        <span className="status-badge atencao">⚠️ Atenção</span>
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