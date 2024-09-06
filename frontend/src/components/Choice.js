import React from 'react';
import { useNavigate } from 'react-router-dom';
import './../App.css'; // Importa o CSS
import axios from "axios";
import './../_assets/css/escolha.css';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;


const Choice = () => {
  const navigate = useNavigate();

  const handleChoicePatientClick = () => {
    navigate('/cadastro-paciente')
  }

  const handleChoiceDoctorClick = () => {
    navigate('/cadastro-medico')
  }

  return (
    <div className="escolha-container">
      {/* Opção Médico */}
      <div className="escolha-opcao escolha-medico">
        <img src={require('./../_assets/img/medico.png')} alt="Médico" className="escolha-imagem medico-img" />
        <button className="escolha-botao" onClick={handleChoiceDoctorClick}>Médico</button>
      </div>

      {/* Texto "ou" */}  
      <div className="escolha-ou">OU</div>

      {/* Opção Paciente */}
      <div className="escolha-opcao escolha-paciente">
        <img src={require('./../_assets/img/paciente.png')} alt="Paciente" className="escolha-imagem paciente-img" />
        <button className="escolha-botao" onClick={handleChoicePatientClick}>Paciente</button>
      </div>
    </div>
  );
};

export default Choice;
