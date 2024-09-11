import React, { useState } from 'react';
import axios from 'axios';
import '../_assets/css/registerDoctor.css'; 

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const RegisterDoctor = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    gender: '',
    telephone: '',
    date_of_birth: '',
    specialty: '',
    crm: '',
    biography: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/register-doctor/', {
        email: formData.email,
        password: formData.password,
        first_name: formData.first_name,
        last_name: formData.last_name,
        gender: parseInt(formData.gender),
        telephone: formData.telephone,
        date_of_birth: formData.date_of_birth,
        specialty: formData.specialty,
        crm: formData.crm,
        biography: formData.biography
      });
      if (response.status === 201) {
        console.log('Doctor registered successfully!');
      } else {
        setError('Registration failed');
      }
    } catch (error) {
      setError('Error connecting to the server');
    }
  };

  return (
    <div className="register-container">
      <div className="register-box">
        <div className="content">
          <div className="logo">
            <img src={require("../_assets/img/logo.png")} alt="Saúde Now" />
          </div>
          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <input
                type="text"
                name="first_name"
                placeholder="Primeiro Nome"
                value={formData.first_name}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="last_name"
                placeholder="Último Nome"
                value={formData.last_name}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="email"
                name="email"
                placeholder="E-mail Acadêmico"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="telephone"
                placeholder="Telefone"
                value={formData.telephone}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="text"
                name="specialty"
                placeholder="Especialidade"
                value={formData.specialty}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="crm"
                placeholder="CRM"
                value={formData.crm}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="text"
                name="biography"
                placeholder="Bibliografia"
                value={formData.biography}
                onChange={handleChange}
                required
              />
              <input
                type="date"
                name="date_of_birth"
                placeholder="Data de Nascimento"
                value={formData.date_of_birth}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-group">
              <input
                type="password"
                name="password"
                placeholder="Senha"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirmar Senha"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>
            <div className="input-group">
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                required
              >
                <option value="">Selecione o Gênero</option>
                <option value="1">Masculino</option>
                <option value="2">Feminino</option>
                <option value="3">Outro</option>
              </select>
            </div>
            {error && <div className="error">{error}</div>}
            <button type="submit" className="register-button">Registrar</button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default RegisterDoctor;
