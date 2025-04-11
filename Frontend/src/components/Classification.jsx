import React from 'react';
import '../styles/classification.css';

const TespitPage = () => {
  return (
    <div className="tespit-page">
      <h1>Tespit Sayfası</h1>
      <p>Güneş paneli fotoğrafınızı yükleyerek segmentasyon yapabilirsiniz.</p>

      <div className="upload-box">
        <input type="file" accept="image/*" />
        <button>Analiz Et</button>
      </div>

    </div>
  );
};

export default TespitPage;
