import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../_assets/css/userProfile.css'; // Importa o CSS

const UserProfile = () => {
    const [userData, setUserData] = useState(null);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:8000/api/user/', {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                setUserData(response.data);
            } catch (error) {
                setError('Erro ao obter dados do usuário');
                console.error(error);
            }
        };

        fetchUserData();
    }, [navigate]);

    if (!userData) {
        return <div>Carregando...</div>;
    }

    return (
        <div className="profile-container">
            <div className="sidebar">
                <img src={require("./../_assets/img/logo.png")} alt="Saúde Now" className="sidebar-logo" />
                <nav>
                    <ul>
                        <li><a href="/inicio">Início</a></li>
                        <li><a href="/medicos">Médicos</a></li>
                        <li><a href="/agenda">Agenda</a></li>
                        <li><a href="/relatorios">Relatórios</a></li>
                        <li><a href="/opcoes">Perfil</a></li>
                    </ul>
                </nav>
                <button onClick={() => navigate('/login')} className="logout-button">Sair</button>
            </div>
            <div className="main-content">
                <header className="header">
                    <h1>Perfil</h1>
                    <div className="user-info">
                        <span>{userData.user_info.first_name} {userData.user_info.last_name}</span>
                        <img src={require('../_assets/img/avatar.png')} alt="User Avatar" className="user-avatar" />
                    </div>
                </header>
                <div className="user-details">
                    <h2>Meus Dados</h2>
                    <div className="user-card">
                        <p><strong>Nome:</strong> {userData.user_info.first_name} {userData.user_info.last_name}</p>
                        <p><strong>Email:</strong> {userData.user_info.email}</p>
                        <p><strong>Gênero:</strong> {userData.user_info.gender === 1 ? 'Masculino' : 'Feminino'}</p>
                    </div>
                    <button onClick={() => navigate('/historico-medico')} className="history-button">Preencher Histórico Médico</button>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
