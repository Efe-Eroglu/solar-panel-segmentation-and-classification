import React, { useState } from 'react';
import '../styles/classification.css';

const TespitPage = () => {
  const [selectedImage, setSelectedImage] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [classificationResult, setClassificationResult] = useState(null);
  const [segmentationResult, setSegmentationResult] = useState(null);
  const [file, setFile] = useState(null);
  const [error, setError] = useState(null);

  const handleImageUpload = async (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      validateAndProcessFile(uploadedFile);
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

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragging(false);
    const uploadedFile = e.dataTransfer.files[0];
    if (uploadedFile) {
      validateAndProcessFile(uploadedFile);
    }
  };

  const validateAndProcessFile = async (uploadedFile) => {
    // Dosya boyutu kontrolü (max 10MB)
    if (uploadedFile.size > 10 * 1024 * 1024) {
      setError("Dosya boyutu çok büyük. Maksimum dosya boyutu 10MB olmalıdır.");
      return;
    }

    // Dosya tipi kontrolü
    const fileType = uploadedFile.type;
    if (!['image/jpeg', 'image/jpg', 'image/png'].includes(fileType)) {
      setError("Sadece JPG, JPEG ve PNG formatları desteklenmektedir.");
      return;
    }

    setError(null);
    setSelectedImage(URL.createObjectURL(uploadedFile));
    setFile(uploadedFile);
    await processImage(uploadedFile);
  };

  const processImage = async (imageFile) => {
    setIsLoading(true);
    setClassificationResult(null);
    setSegmentationResult(null);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', imageFile);

      // Call classification API
      console.log("Sınıflandırma API'sine istek gönderiliyor...");
      const classResponse = await fetch('http://localhost:8000/api/predict-class', {
        method: 'POST',
        body: formData,
      });

      if (!classResponse.ok) {
        const errorData = await classResponse.json();
        throw new Error(`Sınıflandırma hatası: ${errorData.detail || 'Bilinmeyen hata'}`);
      }

      const classData = await classResponse.json();
      console.log("Sınıflandırma sonucu:", classData);
      setClassificationResult(classData);

      // Call segmentation API
      console.log("Segmentasyon API'sine istek gönderiliyor...");
      const segResponse = await fetch('http://localhost:8000/api/segment-image', {
        method: 'POST',
        body: formData,
      });

      if (!segResponse.ok) {
        const errorData = await segResponse.json();
        throw new Error(`Segmentasyon hatası: ${errorData.detail || 'Bilinmeyen hata'}`);
      }

      const segData = await segResponse.json();
      console.log("Segmentasyon sonucu alındı");
      setSegmentationResult(segData);
    } catch (error) {
      console.error('Error processing image:', error);
      setError(`Resim işlenirken bir hata oluştu: ${error.message}`);
    } finally {
      setIsLoading(false);
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
              accept="image/jpeg,image/jpg,image/png" 
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
              <small className="text-muted">PNG, JPG formatları desteklenir (max 10MB)</small>
            </label>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
            </svg>
            <p>{error}</p>
          </div>
        )}

        {isLoading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <p>Resim analiz ediliyor...</p>
          </div>
        )}

        <div className="results-grid">
          <div className="result-card">
            <h3>Sınıflandırma Sonuçları</h3>
            <div className="result-content">
              {classificationResult ? (
                <div className="prediction-details">
                  <h4>Hata Türü: {classificationResult.predicted_class}</h4>
                  <p>Güven Düzeyi: %{(classificationResult.confidence * 100).toFixed(1)}</p>
                  <div className="confidence-meter">
                    <div 
                      className="confidence-fill" 
                      style={{width: `${classificationResult.confidence * 100}%`}}
                    ></div>
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
              {segmentationResult ? (
                <img 
                  src={`data:image/png;base64,${segmentationResult.mask_base64}`} 
                  alt="Segmentasyon sonucu" 
                  style={{maxWidth: '100%', borderRadius: '8px'}}
                />
              ) : selectedImage ? (
                <img 
                  src={selectedImage} 
                  alt="Yüklenen resim" 
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