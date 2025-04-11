import React, { useState } from "react";
import emailjs from "emailjs-com";
import "../styles/contact.css";

const IletisimPage = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    message: "",
  });
  const [status, setStatus] = useState({
    submitting: false,
    success: null,
    message: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus({ submitting: true, success: null, message: "" });
    try {
      await emailjs.send(
        import.meta.env.VITE_EMAILJS_SERVICE_ID,
        import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
        {
          from_name: formData.name,
          from_email: formData.email,
          message: formData.message,
        },
        import.meta.env.VITE_EMAILJS_USER_ID
      );

      setStatus({
        submitting: false,
        success: true,
        message: "Mesajınız başarıyla gönderildi!",
      });
      setFormData({ name: "", email: "", message: "" });

      setTimeout(() => {
        setStatus((prev) => ({ ...prev, message: "" }));
      }, 5000);
    } catch (error) {
      console.error("Gönderim hatası:", error);
      setStatus({
        submitting: false,
        success: false,
        message: "Bir hata oluştu. Lütfen tekrar deneyin.",
      });
    }
  };

  return (
    <div className="iletisim-page">
      <h1>İletişim</h1>
      <p>
        Bizimle iletişime geçmek için formu doldurabilir veya doğrudan eposta
        adresimizden ulaşabilirsiniz.
      </p>

      <form className="contact-form" onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Adınız Soyadınız</label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Adınız Soyadınız"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">E-posta Adresiniz</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="E-posta"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="message">Mesajınız</label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleChange}
            placeholder="Mesajınız"
            required
          />
        </div>

        <button
          type="submit"
          className="submit-btn"
          disabled={status.submitting}
        >
          {status.submitting ? "Gönderiliyor..." : "Gönder"}
        </button>

        {status.message && (
          <div
            className={`status-message ${status.success ? "success" : "error"}`}
          >
            {status.message}
          </div>
        )}
      </form>
    </div>
  );
};

export default IletisimPage;
