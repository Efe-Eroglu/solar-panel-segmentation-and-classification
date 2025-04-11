import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import TespitPage from './components/Classification';
import HakkimizdaPage from './components/AboutUs';
import IletisimPage from './components/Contact';
import NotFound from './components/NotFound';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/classification" element={<TespitPage />} />
        <Route path="/about-us" element={<HakkimizdaPage />} />
        <Route path="/contact" element={<IletisimPage />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App;
