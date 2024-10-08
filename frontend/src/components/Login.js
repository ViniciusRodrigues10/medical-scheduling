import React, { useState } from 'react';
import '../_assets/css/login.css'
import axios from "axios";
import { useNavigate } from 'react-router-dom';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = true;

const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        const loginData = {
            email: email,
            password: password
        };

        try {
            const response = await fetch('http://127.0.0.1:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(loginData)
            });

            if (response.ok) {
                const data = await response.json();
                const token = data.token;
                localStorage.setItem('token', token);

                if(data.user_info.user_type === 2)
                    navigate('/doctor/perfil');
                else
                    navigate('/patient/inicio')
                console.log('Login realizado com sucesso!');
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Erro no login');
            }
        } catch (error) {
            setError('Erro na conexão com o servidor');
        }
    };

    return (
        <div className="login-container">
            <div className="login-box">
                <div className='content'>
                    <div className="logo">
                        <img src={require("./../_assets/img/logo.png")} alt="Saúde Now" className="logo"/>
                    </div>
                <form onSubmit={handleSubmit}>
                    <div className="input-group">
                        <input
                            type="text"
                            placeholder="Email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="input-group">
                        <input
                            type="password"
                            placeholder="Senha"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="link-group">
                        <a href="/escolha">Não é cadastrado? Clique aqui</a>
                    </div>
                    <button type="submit" className="login-button">Entrar</button>
                </form>
                </div>
            </div>
        </div>
    );
};

export default Login;
