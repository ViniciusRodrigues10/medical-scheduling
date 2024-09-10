import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../_assets/css/appointmentPopup.css';

const AppointmentPopup = ({ onClose, onBook }) => {
    const [specialties, setSpecialties] = useState([]);
    const [selectedSpecialty, setSelectedSpecialty] = useState('');
    const [availability, setAvailability] = useState([]);
    const [selectedTime, setSelectedTime] = useState('');

    useEffect(() => {
        const fetchSpecialties = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/specialties/');
                setSpecialties(response.data.specialties);
            } catch (error) {
                console.error('Erro ao obter especialidades', error);
            }
        };

        fetchSpecialties();
    }, []);

    useEffect(() => {
        if (selectedSpecialty) {
            const fetchAvailability = async () => {
                try {
                    const response = await axios.get(`http://localhost:8000/api/availability/${selectedSpecialty}/`);
                    setAvailability(response.data);
                } catch (error) {
                    console.error('Erro ao obter disponibilidade', error);
                }
            };

            fetchAvailability();
        }
    }, [selectedSpecialty]);

    const handleBookAppointment = async () => {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                alert('Você precisa estar logado para agendar uma consulta');
                return;
            }

            const [doctor_first_name, doctor_last_name] = selectedTime.split(',')[0].split(' ');
            const [date, start_time] = selectedTime.split(',')[1].split(' ');
            const appointmentData = {
                doctor_first_name,
                doctor_last_name,
                date,
                start_time
            };
            await axios.post('http://localhost:8000/api/appointment/book/', appointmentData, {
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json'
                }
            });
            onBook(); // Call the onBook function to refresh the appointments list
            onClose(); // Close the popup
        } catch (error) {
            console.error('Erro ao agendar consulta', error);
        }
    };

    return (
        <div className="popup-overlay">
            <div className="popup">
                <h2>Agendar Consulta</h2>
                <div className="form-group">
                    <label>Especialidade:</label>
                    <select
                        value={selectedSpecialty}
                        onChange={(e) => setSelectedSpecialty(e.target.value)}
                    >
                        <option value="">Selecione uma especialidade</option>
                        {specialties.map((specialty) => (
                            <option key={specialty} value={specialty}>
                                {specialty}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label>Horário Disponível:</label>
                    <select
                        value={selectedTime}
                        onChange={(e) => setSelectedTime(e.target.value)}
                        disabled={!selectedSpecialty}
                    >
                        <option value="">Selecione um horário</option>
                        {availability.map((slot, index) => (
                            <option key={index} value={`${slot.doctor_first_name} ${slot.doctor_last_name},${slot.date} ${slot.start_time}`}>
                                {slot.date} {slot.start_time} - {slot.end_time} ({slot.doctor_first_name} {slot.doctor_last_name})
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <button onClick={handleBookAppointment}>Agendar</button>
                    <button onClick={onClose}>Cancelar</button>
                </div>
            </div>
        </div>
    );
};

export default AppointmentPopup;
