import React, { useState, useEffect, useRef } from 'react';

// Helper function to check and fix base64 strings
const ensureCompleteBase64 = (base64String) => {
  if (!base64String) return '';
  
  // Check if the base64 string is properly padded
  const paddingNeeded = (4 - (base64String.length % 4)) % 4;
  if (paddingNeeded > 0) {
    return base64String + '='.repeat(paddingNeeded);
  }
  return base64String;
};

const Segmentation = ({ maskUrl, overlayUrl, activeTab = 'overlay', onTabChange }) => {
  const [isImageLoaded, setIsImageLoaded] = useState(false);
  const [canvasError, setCanvasError] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const maskCanvasRef = useRef(null);

  // Reset state when switching tabs
  useEffect(() => {
    setIsImageLoaded(false);
  }, [activeTab]);

  // Mask görüntüsünü işleme - URL'den çekip canvas'a çizme
  useEffect(() => {
    if (activeTab === 'mask' && maskUrl && maskCanvasRef.current) {
      setIsProcessing(true);

      try {
        const canvas = maskCanvasRef.current;
        const ctx = canvas.getContext('2d');
        
        // Yeni bir görüntü oluştur
        const img = new Image();
        img.crossOrigin = 'anonymous'; // CORS sorunlarını önle
        
        img.onload = () => {
          // Canvas boyutlarını ayarla
          canvas.width = img.width;
          canvas.height = img.height;
          
          // Canvas'ı temizle
          ctx.fillStyle = 'black';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          
          // Görüntüyü çiz ve işle
          ctx.globalCompositeOperation = 'screen';
          ctx.drawImage(img, 0, 0);
          
          // Piksel işleme için görüntü verilerini al
          const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
          const data = imageData.data;
          
          // Her pikseli işle - siyah ve beyazı daha belirgin hale getir
          for (let i = 0; i < data.length; i += 4) {
            // Pikselin herhangi bir değere sahip olup olmadığını kontrol et
            if (data[i] > 10 || data[i+1] > 10 || data[i+2] > 10) {
              // Beyaz yap
              data[i] = 255;     // R
              data[i + 1] = 255; // G
              data[i + 2] = 255; // B
            } else {
              // Siyah yap
              data[i] = 0;     // R
              data[i + 1] = 0; // G
              data[i + 2] = 0; // B
            }
            // Alfa kanalını olduğu gibi bırak
          }
          
          // İşlenmiş görüntü verilerini canvas'a geri koy
          ctx.putImageData(imageData, 0, 0);
          
          setIsImageLoaded(true);
          setIsProcessing(false);
        };
        
        img.onerror = () => {
          console.error('Mask image loading error');
          setCanvasError(true);
          setIsProcessing(false);
        };
        
        // Resmi URL'den yükle
        img.src = maskUrl;
      } catch (err) {
        console.error('Canvas error:', err);
        setCanvasError(true);
        setIsProcessing(false);
      }
    }
  }, [activeTab, maskUrl]);

  // Handle download of the images
  const handleDownloadImage = () => {
    try {
      // Blob URL'leri doğrudan indiremeyiz, fetch ile alıp sonra indirmeliyiz
      const downloadUrl = activeTab === 'mask' ? maskUrl : overlayUrl;
      
      if (downloadUrl) {
        // Yeni sekme açarak görüntüyü göster - kullanıcı buradan kaydedebilir
        window.open(downloadUrl, '_blank');
      }
    } catch (err) {
      console.error('Download error:', err);
    }
  };

  return (
    <div className="segmentation-result">
      <div className="segmentation-image">
        <div className="image-tabs">
          <button 
            className={activeTab === 'overlay' ? 'active' : ''} 
            onClick={() => onTabChange('overlay')}
          >
            Hasarlı Bölgeler
          </button>
          <button 
            className={activeTab === 'mask' ? 'active' : ''} 
            onClick={() => onTabChange('mask')}
          >
            Maske Haritası
          </button>
        </div>
        <div 
          className={activeTab === 'mask' ? 'darkroom-bg' : ''}
          style={{ 
            background: activeTab === 'mask' ? '#000' : 'transparent',
          }}
        >
          {isProcessing && (
            <div className="processing-indicator">
              <div className="spinner-small"></div>
              <p>Görüntü işleniyor...</p>
            </div>
          )}
          
          {activeTab === 'overlay' ? (
            // Overlay görüntüsünü doğrudan URL'den göster
            <img 
              src={overlayUrl}
              alt="Overlay görüntüsü" 
              style={{
                maxWidth: '100%', 
                display: 'block',
                margin: '0 auto',
                opacity: isImageLoaded ? 1 : 0,
                transition: 'opacity 0.3s ease'
              }}
              onLoad={() => setIsImageLoaded(true)}
            />
          ) : (
            // İşlenmiş maske görüntüsünü canvas üzerinde göster
            <canvas 
              ref={maskCanvasRef}
              style={{
                maxWidth: '100%',
                display: 'block',
                margin: '0 auto',
                opacity: isImageLoaded ? 1 : 0,
                transition: 'opacity 0.3s ease'
              }}
            />
          )}
        </div>
        
        {activeTab === 'mask' && (
          <div className="mask-legend">
            <p>
              <span style={{ 
                display: 'inline-block', 
                width: '12px', 
                height: '12px', 
                backgroundColor: '#fff', 
                marginRight: '5px', 
                border: '1px solid #ddd',
                borderRadius: '2px'
              }}></span>
              Beyaz alanlar tespit edilen bölgeleri, siyah alanlar normal bölgeleri gösterir.
            </p>
          </div>
        )}
        
        {(activeTab === 'mask' && maskUrl) || (activeTab === 'overlay' && overlayUrl) ? (
          <div className="mask-actions">
            <button 
              className="download-button"
              onClick={handleDownloadImage}
            >
              Görüntüyü Aç
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
                <polyline points="15 3 21 3 21 9"></polyline>
                <line x1="10" y1="14" x2="21" y2="3"></line>
              </svg>
            </button>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default Segmentation; 