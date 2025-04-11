import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import TespitPage from './components/Classification';
import HakkimizdaPage from './components/AboutUs';
import IletisimPage from './components/Contact';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/tespit" element={<TespitPage />} />
        <Route path="/hakkimizda" element={<HakkimizdaPage />} />
        <Route path="/iletisim" element={<IletisimPage />} />
      </Routes>
    </Router>
  );
}

export default App;
