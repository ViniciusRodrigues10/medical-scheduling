import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu';
import '../_assets/css/agenda.css';

const History = () => {
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const fetchAppointments = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await axios.get('http://localhost:8000/api/user/query-history/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            setAppointments(response.data);
        } catch (error) {
            setError('Erro ao obter histórico de consultas');
            console.error(error);
        }
    };

    useEffect(() => {
        fetchAppointments();
    }, [navigate]);

    return (
        <div className="profile-container">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h1>Histórico de Consultas</h1>
                </header>
                <div className="appointments-container">
                    {error && <p className="error-message">{error}</p>}
                    {appointments.length === 0 ? (
                        <p>Não há histórico de consultas.</p>
                    ) : (
                        <ul className="appointments-list">
                            {appointments.map((appointment) => (
                                <li key={appointment.id_appointment}>
                                    <p className="specialty">{appointment.doctor_specialty}</p>
                                    <p><strong>Médico:</strong> {appointment.doctor_first_name} {appointment.doctor_last_name}</p>
                                    <p><strong>Data:</strong> {appointment.date}</p>
                                    <p><strong>Hora:</strong> {appointment.start_time} - {appointment.end_time}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
};

export default History;
