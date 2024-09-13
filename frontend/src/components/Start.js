import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Sidebar from './Menu';
import '../_assets/css/start.css'; // Adicione o seu CSS para estilizar a página

const Dashboard = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    // Redirecionar para login se o token não estiver presente
                    window.location.href = '/login';
                    return;
                }

                const response = await axios.get('http://localhost:8000/api/user/main-data/', {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                setData(response.data);
            } catch (err) {
                setError('Erro ao carregar dados');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return <div className="loading">Carregando...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="dashboard-container">
            <Sidebar />
            <div className="main-content">
                <header className="dashboard-header">
                    <h1>Bem-vindo, {data.user_info.first_name}!</h1>
                </header>
                <div className="dashboard-content">
                    <div className="info-box">
                        <h2>Informações do Usuário</h2>
                        <div className="user-info-table">
                            <p><strong>Email:</strong> {data.user_info.email}</p>
                            <p><strong>Nome:</strong> {data.user_info.first_name} {data.user_info.last_name}</p>
                            <p><strong>Tipo de Usuário:</strong> {data.user_info.user_type}</p>
                        </div>
                    </div>
                    <div className="info-box">
                        <h2>Consultas</h2>
                        <div className="appointments-info-content">
                            <p><strong>Consultas Futuras:</strong> {data.future_appointments}</p>
                            <p><strong>Consultas Passadas:</strong> {data.past_appointments}</p>
                        </div>
                    </div>
                    <div className="info-box">
                        <h2>Médicos Disponíveis</h2>
                        <div className="doctors-info-content">
                            <p>{data.doctors_count}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
