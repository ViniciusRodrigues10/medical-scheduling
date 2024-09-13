import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu';
import AppointmentPopup from './AppointmentPopup';
import Modal from 'react-modal';
import '../_assets/css/agenda.css';

Modal.setAppElement('#root');

const Schedule = () => {
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState('');
    const [showPopup, setShowPopup] = useState(false);
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [selectedAppointment, setSelectedAppointment] = useState(null);
    const navigate = useNavigate();

    const fetchAppointments = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await axios.get('http://localhost:8000/api/user/appointments/', {
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

    const deleteAppointment = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        if (selectedAppointment) {
            try {
                await axios.delete('http://127.0.0.1:8000/api/delete-appointment/', {
                    headers: {
                        'Authorization': `Token ${token}`
                    },
                    data: {
                        date: selectedAppointment.date,
                        start_time: selectedAppointment.start_time
                    }
                });
                setAppointments(appointments.filter(a => a.id_appointment !== selectedAppointment.id_appointment));
                setSelectedAppointment(null);
            } catch (error) {
                setError('Erro ao excluir agendamento');
                console.error(error);
            }
        }
        closeModal();
    };

    useEffect(() => {
        fetchAppointments();
    }, [navigate]);

    const openModal = (appointment) => {
        setSelectedAppointment(appointment);
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
        setSelectedAppointment(null);
    };

    return (
        <div className="profile-container">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h1>Consultas Marcadas</h1>
                    <button onClick={() => setShowPopup(true)} className="schedule-button">Agendar Consulta</button>
                </header>
                <div className="appointments-container">
                    {error && <p className="error-message">{error}</p>}
                    {appointments.length === 0 ? (
                        <p className="no-schedule-appointments-message">Não há agendamentos.</p>
                    ) : (
                        <ul className="appointments-list">
                            {appointments.map((appointment) => (
                                <li key={appointment.id_appointment}>
                                    <p className="specialty">{appointment.doctor_specialty}</p>
                                    <p><strong>Médico:</strong> {appointment.doctor_first_name} {appointment.doctor_last_name}</p>
                                    <p><strong>Data:</strong> {appointment.date}</p>
                                    <p><strong>Hora:</strong> {appointment.start_time} - {appointment.end_time}</p>
                                    <button 
                                        className="delete-button"
                                        onClick={() => openModal(appointment)}
                                    >
                                        Desmarcar
                                    </button>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
            {showPopup && (
                <AppointmentPopup
                    onClose={() => setShowPopup(false)}
                    onBook={fetchAppointments}
                />
            )}
            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel="Confirmação de Exclusão"
                className="modal"
                overlayClassName="overlay"
            >
                <h2>Tem certeza que deseja desmarcar a consulta?</h2>
                <button onClick={deleteAppointment} className="confirm-button">Sim</button>
                <button onClick={closeModal} className="cancel-button">Não</button>
            </Modal>
        </div>
    );
};

export default Schedule;
