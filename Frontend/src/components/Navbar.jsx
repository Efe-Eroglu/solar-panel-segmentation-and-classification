import React from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="logo">SolarVision</div>
      <ul className="nav-links">
        <li><NavLink to="/" end>Anasayfa</NavLink></li>
        <li><NavLink to="/tespit">Tespit</NavLink></li>
        <li><NavLink to="/hakkimizda">Hakkımızda</NavLink></li>
        <li><NavLink to="/iletisim">İletişim</NavLink></li>
      </ul>
    </nav>
  );
};

export default Navbar;
