import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import '../_assets/css/registerPatient.css'; // Importa o CSS
import axios from 'axios';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const RegisterPatient = () => {
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        email: '',
        password: '',
        confirmPassword: '',
        gender: 1 // Default to "male"
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setSuccess('');

        if (formData.password !== formData.confirmPassword) {
            setError('As senhas não coincidem');
            return;
        }

        const registrationData = {
            email: formData.email,
            password: formData.password,
            first_name: formData.firstName,
            last_name: formData.lastName,
            gender: parseInt(formData.gender, 10) // Converta para número
        };

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/register-patient/', registrationData, {
                headers: {
                    'Content-Type': 'application/json',
                },
                withCredentials: true,
            });

            if (response.status === 201) {
                setSuccess('Cadastro realizado com sucesso!');
                navigate('/login');
            } else {
                setError('Erro ao registrar. Tente novamente.');
            }
        } catch (error) {
            console.error('Erro:', error.response ? error.response.data : error.message);
            setError('Erro na conexão com o servidor');
        }
    };

    return (
        <div className="register-container">
            <div className="register-box">
                <div className="logo">
                    <img src={require('../_assets/img/logo.medical.jpeg')} alt="Saúde Now" className="logo" />
                </div>
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <input
                            type="text"
                            name="firstName"
                            placeholder="Primeiro Nome"
                            value={formData.firstName}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="text"
                            name="lastName"
                            placeholder="Último Nome"
                            value={formData.lastName}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="email"
                            name="email"
                            placeholder="Email Acadêmico"
                            value={formData.email}
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
                    </div>
                    <div className="input-group">
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
                        <label htmlFor="gender">Gênero:</label>
                        <select
                            name="gender"
                            value={formData.gender}
                            onChange={handleChange}
                            required
                        >
                            <option value="1">Masculino</option>
                            <option value="2">Feminino</option>
                            <option value="3">Outro</option>
                        </select>
                    </div>
                    {error && <p className="error">{error}</p>}
                    {success && <p className="success">{success}</p>}
                    <button type="submit" className="register-button">Registrar</button>
                </form>
            </div>
        </div>
    );
};

export default RegisterPatient;
