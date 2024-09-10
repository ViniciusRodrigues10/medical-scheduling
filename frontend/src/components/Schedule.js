import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu'; // Importa a função da barra lateral
import '../_assets/css/agenda.css'; // Importa o CSS

const Schedule = () => {
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchAppointments = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await axios.get('http://127.0.0.1:8000/api/appointments/future', {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                setAppointments(response.data);
            } catch (error) {
                setError('Erro ao obter agendamentos');
                console.error(error);
            }
        };

        fetchAppointments();
    }, [navigate]);

    return (
        <div className="profile-container">
            {/* Adiciona a barra lateral importada */}
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h1>Agendamentos Futuras</h1>
                </header>
                <div className="appointments-container">
                    {appointments.length === 0 ? (
                        <p>Não há agendamentos futuros.</p>
                    ) : (
                        <ul className="appointments-list">
                            {appointments.map((appointment) => (
                                <li key={appointment.id_appointment}>
                                    <p><strong>Data:</strong> {appointment.date}</p>
                                    <p><strong>Hora:</strong> {appointment.start_time} - {appointment.end_time}</p>
                                    <p><strong>Especialidade:</strong> {appointment.doctor_specialty}</p>
                                    <p><strong>Médico:</strong> {appointment.doctor_first_name} {appointment.doctor_last_name}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                    <button onClick={() => navigate('/agendar-consulta')} className="schedule-button">Agendar Consulta</button>
                </div>
            </div>
        </div>
    );
};

export default Schedule;
