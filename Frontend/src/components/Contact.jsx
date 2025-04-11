import React from 'react';
import '../styles/contact.css';

const IletisimPage = () => {
  return (
    <div classN ame="iletisim-page">
      <h1>İletişim</h1>
      <p>Bizimle iletişime geçmek için formu doldurabilirsiniz.</p>

      <form className="contact-form">
        <input type="text" placeholder="Adınız Soyadınız" required />
        <input type="email" placeholder="E-posta" required />
        <textarea placeholder="Mesajınız" rows="5" required></textarea>
        <button type="submit">Gönder</button>
      </form>
    </div>
  );
};

export default IletisimPage;
