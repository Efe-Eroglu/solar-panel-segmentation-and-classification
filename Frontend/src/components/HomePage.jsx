import React from 'react';
import Hero from './Hero';
import '../styles/homePage.css';

const HomePage = () => {
  return (
    <div className="home-page">
      <Hero />
      <section className="features">
        <h2>Özellikler</h2>
        <div className="feature-grid">
          <div className="feature-box">Gerçek zamanlı analiz</div>
          <div className="feature-box">Gelişmiş segmentasyon</div>
          <div className="feature-box">Hata türü sınıflandırması</div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
