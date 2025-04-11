import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/notFound.css';

const NotFound = () => {
  return (
    <div className="notfound-container">
      <h1>404 - Sayfa Bulunamadı</h1>
      <p>Aradığınız sayfa mevcut değil. Ana sayfaya dönebilirsiniz.</p>
      <Link to="/" className="notfound-btn">Anasayfa</Link>
    </div>
  );
};

export default NotFound;
