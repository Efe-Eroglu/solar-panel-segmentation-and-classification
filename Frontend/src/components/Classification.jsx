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
  const [imageStats, setImageStats] = useState(null);

  // Sınıf adlarını doğru sırayla tanımlayalım
  const classNames = ["normal", "bird-drop", "dusty", "electrical-damage", "faulty", "snow-covered"];

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
    
    // Dosya istatistiklerini ayarla
    const fileSizeKB = (uploadedFile.size / 1024).toFixed(2);
    const fileSizeMB = (uploadedFile.size / (1024 * 1024)).toFixed(2);
    const fileDate = new Date(uploadedFile.lastModified).toLocaleString();
    
    setImageStats({
      name: uploadedFile.name,
      size: `${fileSizeKB} KB (${fileSizeMB} MB)`,
      type: uploadedFile.type,
      lastModified: fileDate
    });
    
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

  // Sınıflandırma sonucuna göre hata sınıfının açıklamasını döndürür
  const getClassDescription = (className) => {
    const descriptions = {
      "normal": "Panel normal durumda, herhangi bir hata tespit edilmedi.",
      "bird-drop": "Panel üzerinde kuş pisliği var, kısmi gölgelenme oluşturuyor.",
      "dusty": "Panel üzerinde toz birikintisi var, temizlik gerekli olabilir.",
      "electrical-damage": "Panel üzerinde elektriksel hasar veya bozulma tespit edildi.",
      "faulty": "Panel üzerinde genel bir hata tespit edildi.",
      "snow-covered": "Panel kar ile kaplı, elektrik üretimi düşük olabilir."
    };
    return descriptions[className] || "Bilinmeyen hata tipi";
  };

  // Sınıf adına göre önerilen çözüm
  const getRecommendation = (className) => {
    const recommendations = {
      "normal": "Herhangi bir işlem gerekmemektedir.",
      "bird-drop": "Panel yüzeyi temizlenmelidir. Tekrarını önlemek için kuş engelleyici önlemler alınabilir.",
      "dusty": "Düzenli temizlik yapılmalıdır. Otomatik temizleme sistemleri değerlendirilebilir.",
      "electrical-damage": "Acil servis müdahalesi gereklidir. Paneli kullanmayı durdurun.",
      "faulty": "Panelin detaylı inceleme için servis çağırmanız önerilir.",
      "snow-covered": "Karın temizlenmesi için güvenli bir şekilde panele müdahale edilmelidir."
    };
    return recommendations[className] || "Uzman değerlendirmesi gerekli";
  };

  // Sınıf adını Türkçe olarak göster
  const getClassNameTurkish = (className) => {
    const turkishNames = {
      "normal": "Normal",
      "bird-drop": "Kuş Pisliği",
      "dusty": "Tozlu",
      "electrical-damage": "Elektriksel Hasar",
      "faulty": "Hasarlı",
      "snow-covered": "Kar Kaplı"
    };
    return turkishNames[className] || className;
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
                  <h4>Hata Türü: {getClassNameTurkish(classificationResult.predicted_class)}</h4>
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
                <div className="segmentation-result">
                  <div className="segmentation-image">
                    <img 
                      src={`data:image/png;base64,${segmentationResult.mask_base64}`} 
                      alt="Segmentasyon sonucu" 
                      style={{maxWidth: '100%', borderRadius: '8px'}}
                    />
                  </div>
                  <div className="segmentation-overlay" style={{position: 'relative', marginTop: '10px'}}>
                    <p className="segmentation-info">
                      <strong>Segmentasyon Açıklaması:</strong> {segmentationResult.description}
                    </p>
                    <p className="segmentation-tip">
                      <small>Segmentasyon maskeleri, panellerin üzerindeki hasarlı bölgeleri vurgular.</small>
                    </p>
                  </div>
                </div>
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

        {/* Ek Metrikler ve Detaylar */}
        {(classificationResult || imageStats) && (
          <div className="metrics-section">
            <h3>Detaylı Analiz Sonuçları</h3>
            
            {imageStats && (
              <div className="metric-card">
                <h4>Görüntü Bilgileri</h4>
                <div className="metrics-grid">
                  <div className="metric-item">
                    <span className="metric-label">Dosya Adı:</span>
                    <span className="metric-value">{imageStats.name}</span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">Dosya Boyutu:</span>
                    <span className="metric-value">{imageStats.size}</span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">Dosya Tipi:</span>
                    <span className="metric-value">{imageStats.type}</span>
                  </div>
                  <div className="metric-item">
                    <span className="metric-label">Son Değişiklik:</span>
                    <span className="metric-value">{imageStats.lastModified}</span>
                  </div>
                </div>
              </div>
            )}

            {classificationResult && (
              <div className="metric-card">
                <h4>Tüm Sınıflandırma Sonuçları</h4>
                <div className="class-bars">
                  {classNames.map((cls) => {
                    // API'den gelen gerçek olasılık değerlerini kullan
                    const probability = classificationResult.all_probabilities[cls] || 0;
                    const isActive = cls === classificationResult.predicted_class;
                    
                    return (
                      <div key={cls} className={`class-bar-item ${isActive ? 'active' : ''}`}>
                        <div className="class-bar-label">{getClassNameTurkish(cls)}</div>
                        <div className="class-bar-container">
                          <div 
                            className="class-bar-fill" 
                            style={{width: `${probability * 100}%`}}
                          ></div>
                          <span className="class-bar-value">{(probability * 100).toFixed(1)}%</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        )}
      </section>
    </div>
  );
};

export default TespitPage;