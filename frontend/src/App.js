import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/home'; 
import RegisterPatient from './components/registerPatient';
import RegisterDoctor from './components/RegisterDoctor';
import Login from './components/Login';
import Choice from './components/Choice';
import UserProfile from './components/UserProfile';
import MedicalHistoryForm from './components/MedicalHistoryForm';
import Schedule from './components/Schedule';

// import Home from './components/Home'; // Exemplo de outra página

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} /> 
        <Route path="/cadastro-paciente" element={<RegisterPatient />} />
        <Route path="/cadastro-medico" element={<RegisterDoctor />} />
        <Route path="/historico-medico" element={<MedicalHistoryForm />} />
        <Route path="/login" element={<Login />} />
        <Route path="/perfil" element={<UserProfile />} />
        <Route path="/escolha" element={<Choice />} />
        <Route path="/agenda" element={<Schedule />} />
      </Routes>
    </Router>
  );
}

export default App;