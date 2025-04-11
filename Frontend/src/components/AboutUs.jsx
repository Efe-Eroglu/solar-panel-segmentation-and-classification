import React, { useEffect } from "react";
import "../styles/about.css";

const teamMembers = [
  {
    name: "Efe Eroğlu",
    role: "Yapay Zeka Geliştiricisi",
    bio: "Makine öğrenmesi ve derin öğrenme alanında deneyim",
    photo: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTd0qLNKg1xkfwlWSofzVb7fn8p-prrv7xgmQ&s",
    social: {
      linkedin: "https://www.linkedin.com/in/efeeroglu/",
      github: "https://github.com/Efe-Eroglu",
      website: "https://efe-eroglu.github.io/",
    },
  },
];

const HakkimizdaPage = () => {
  useEffect(() => {
    const handleScroll = () => {
      const elements = document.querySelectorAll(".team-card, .stat-item");
      elements.forEach((el) => {
        const elementTop = el.getBoundingClientRect().top;
        if (elementTop < window.innerHeight * 0.8) {
          el.style.opacity = 1;
          el.style.transform = "translateY(0)";
        }
      });
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <div className="hakkimizda-page">
      <section className="about-hero">
        <h1>Enerjinin Geleceğini Şekillendiriyoruz</h1>
        <p>
          SolarVision, güneş enerjisi sistemlerinde oluşabilecek panel
          hatalarını tespit eden, yapay zeka destekli analiz çözümleri sunan
          yenilikçi bir projedir.
        </p>
        <p>
          Ekibimiz; yapay zeka, yazılım mühendisliği ve yenilenebilir enerji
          alanında uzmanlaşmış gençlerden oluşmaktadır.
        </p>
      </section>

      <div className="stats-grid">
        <div className="stat-item" style={{ animationDelay: "0.2s" }}>
          <div className="stat-number">10K+</div>
          <div className="stat-label">Analiz Edilen Panel</div>
        </div>
        <div className="stat-item" style={{ animationDelay: "0.4s" }}>
          <div className="stat-number">%98.7</div>
          <div className="stat-label">Doğruluk Oranı</div>
        </div>
        <div className="stat-item" style={{ animationDelay: "0.6s" }}>
          <div className="stat-number">50+</div>
          <div className="stat-label">Mutlu Müşteri</div>
        </div>
      </div>

      <section className="team-section">
        <h2 className="section-title">Ekibimiz</h2>
        {teamMembers.map((member, index) => (
          <div key={index} className="team-card">
            <img src={member.photo} alt={member.name} className="team-photo" />
            <h3>{member.name}</h3>
            <p className="role">{member.role}</p>
            <p className="bio">{member.bio}</p>
            <div className="social-links">
              <a href={member.social.linkedin} aria-label="LinkedIn" target="_blank">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                  <rect x="2" y="9" width="4" height="12"></rect>
                  <circle cx="4" cy="4" r="2"></circle>
                </svg>
              </a>
              <a href={member.social.github} aria-label="GitHub" target="_blank">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
                </svg>
              </a>
              <a href={member.social.website} aria-label="Website" target="_blank">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                >
                  <circle cx="12" cy="12" r="10" />
                  <line x1="2" y1="12" x2="22" y2="12" />
                  <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                </svg>
              </a>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
};

export default HakkimizdaPage;
