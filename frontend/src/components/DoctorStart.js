import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Sidebar from './DoctorMenu';
import '../_assets/css/start.css'; // Adicione o seu CSS para estilizar a página

const DoctorDashboard = () => {
    const [appointmentsCount, setAppointmentsCount] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchAppointments = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    window.location.href = '/login';
                    return;
                }

                // Faz a requisição para o endpoint de consultas do médico
                const response = await axios.get('http://localhost:8000/api/doctor-appointments/', {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });

                setAppointmentsCount(response.data.length); // Assume que o endpoint retorna uma lista de consultas
            } catch (err) {
                setError('Erro ao carregar consultas');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchAppointments();
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
                    <h1>Bem-vindo, Médico!</h1>
                </header>
                <div className="dashboard-content">
                    <div className="info-box">
                        <h2>Consultas</h2>
                        <p><strong>Total de Consultas Marcadas:</strong> {appointmentsCount}</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DoctorDashboard;
