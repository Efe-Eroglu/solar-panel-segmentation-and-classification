import React from 'react';
import '../styles/hero.css';
import heroImage from '../assets/hero.jpg';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-text">
        <h1>Güneş Paneli Hatalarını Anında Tespit Edin</h1>
        <p>Gelişmiş segmentasyon algoritmaları ile panellerinizi analiz edin, sorunları erkenden keşfedin.</p>
        <button>Başlayın</button>
      </div>
      <img src={heroImage} alt="Hero Görseli" className="hero-image" />
    </section>
  );
};

export default Hero;
