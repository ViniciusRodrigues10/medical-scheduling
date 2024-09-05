/*import React, { useState } from "react";
import axios from "axios";
import './App.css'; // Importa o CSS

// Configuração do Axios
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const HomePage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/api/login/", {
        email,
        password,
      });

      // Sucesso no login
      console.log(response.data);
      // Ações adicionais, como salvar token, redirecionar, etc.
    } catch (error) {
      setError("Falha no login. Verifique suas credenciais e tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <nav className="navbar">
        <a href="/sobre" className="nav-link">Sobre</a>
        <a href="/medicos" className="nav-link">Nossos Médicos</a>
      </nav>
      <div className="content">
        <div className="background-panel"></div> {/* Adicionando fundo branco esbranquiçado *//*}
        <div className="white-panel">
          <div className="logo">
            <img 
              src={require('./_assets/img/logo.medical.jpeg')} />
          </div>
          <button className="btn-entrar">Entrar</button>
          <p>OU</p>
          <a href="#criar-conta" className="link-criar-conta">Criar Conta</a>
        </div>
      </div>
    </div>
  );
};

export default HomePage;*/

// import React from 'react';
// import Login from './Login';

// function App() {
//   return (
//     <div className="App">
//       <Login />
//     </div>
//   );
// }

// export default App;

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/home'; 
import RegisterPatient from './components/registerPatient';
import Login from './Login';
// import Home from './components/Home'; // Exemplo de outra página

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route path="/register" element={<RegisterPatient />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;