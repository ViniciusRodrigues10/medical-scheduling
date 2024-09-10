import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu'; 
import '../_assets/css/userProfile.css';

const UserProfile = () => {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
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
                setLoading(false);
            } catch (error) {
                setError('Erro ao obter dados do usuário');
                console.error(error);
                setLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    return (
        <div className="profile-container">
            <Sidebar /> 
            <div className="main-content">
                <header className="header">
                    <h1>Perfil</h1>
                    <div className="user-info">
                        <span>{userData?.user_info.first_name} {userData?.user_info.last_name}</span>
                        <img src={require('../_assets/img/icone-perfil.png')} alt="User Avatar" className="user-perfil" />
                    </div>
                </header>
                <div className="user-details">
                    {loading ? (
                        <p>Carregando...</p>
                    ) : error ? (
                        <p className="error-message">{error}</p>
                    ) : (
                        <>
                            <h2>Meus Dados</h2>
                            <div className="user-card">
                                <p><strong>Nome:</strong> {userData.user_info.first_name} {userData.user_info.last_name}</p>
                                <p><strong>Email:</strong> {userData.user_info.email}</p>
                                <p><strong>Gênero:</strong> {userData.user_info.gender === 1 ? 'Masculino' : 'Feminino'}</p>
                            </div>
                            <button onClick={() => navigate('/historico-medico')} className="history-button">Preencher Histórico Médico</button>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
