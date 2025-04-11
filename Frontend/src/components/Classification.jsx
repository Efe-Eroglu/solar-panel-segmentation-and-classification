import React, { useState } from 'react';
import '../styles/classification.css';

const TespitPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      setSelectedImage(URL.createObjectURL(file));
    }
  };

  return (
    <div className="tespit-page">
      <section className="upload-section">
        <h1>Güneş Paneli Analizi</h1>
        <p>Yüksek hassasiyetli AI modelimizle panel hatalarını anında tespit edin</p>

        <div 
          className={`upload-box ${isDragging ? 'dragover' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="custom-upload">
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleImageUpload}
              id="file-upload"
            />
            <label htmlFor="file-upload" className="upload-label">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
              </svg>
              <span>Dosyanızı sürükleyip bırakın veya</span>
              <button className="upload-button" type="button">
                Dosya Seçin
              </button>
              <small className="text-muted">PNG, JPG formatları desteklenir</small>
            </label>
          </div>
        </div>

        <div className="results-grid">
          <div className="result-card">
            <h3>Sınıflandırma Sonuçları</h3>
            <div className="result-content">
              {selectedImage ? (
                <div className="prediction-details">
                  <h4>Hata Türü: Mikroçatlak</h4>
                  <p>Güven Düzeyi: %92.4</p>
                  <div className="confidence-meter">
                    <div className="confidence-fill" style={{width: '92.4%'}}></div>
                  </div>
                </div>
              ) : (
                <div className="result-placeholder">Analiz sonuçları burada görüntülenecek</div>
              )}
            </div>
          </div>

          <div className="result-card">
            <h3>Segmentasyon Sonuçları</h3>
            <div className="result-content">
              {selectedImage ? (
                <img 
                  src={selectedImage} 
                  alt="Segmentasyon sonucu" 
                  style={{maxWidth: '100%', borderRadius: '8px'}}
                />
              ) : (
                <div className="result-placeholder">Segmentasyon haritası burada görüntülenecek</div>
              )}
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default TespitPage;