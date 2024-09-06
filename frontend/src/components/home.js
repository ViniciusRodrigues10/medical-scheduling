import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../_assets/css/home.css';

const HomePage = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    navigate('/login');
  };

  const handleRegisterClick = () => {
    navigate('/register');
  };

  return (
    <div className="container">
      <nav className="navbar">
        <a href="/sobre" className="nav-link">Sobre</a>
        <a href="/medicos" className="nav-link">Nossos Médicos</a>
      </nav>
      <div className="content">
        <div className="background-panel"></div> {/* Adicionando fundo branco esbranquiçado */}
        <div className="white-panel">
          <div className="logo">
            <img src={require('../_assets/img/logo.medical.jpeg')} alt="Saúde Now" className="logo" />
          </div>
          <button className="btn-entrar" onClick={handleLoginClick}>Entrar</button>
          <p>OU</p>
          <a href="#criar-conta" className="link-criar-conta" onClick={handleRegisterClick}>Criar Conta</a>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
