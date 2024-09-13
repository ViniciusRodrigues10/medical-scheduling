import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu';
import '../_assets/css/availability.css';

const AvailabilityManager = () => {
    const [availabilities, setAvailabilities] = useState([]);
    const [newAvailability, setNewAvailability] = useState({
        date: '',
        start_time: '',
        end_time: ''
    });
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
    const [minTime, setMinTime] = useState('');
    const navigate = useNavigate();

    // Função para buscar horários disponíveis
    const fetchAvailabilities = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await axios.get('http://127.0.0.1:8000/api/availability-list/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });

            const filteredAvailabilities = filterFutureAvailabilities(response.data);
            setAvailabilities(filteredAvailabilities);
        } catch (error) {
            setError('Erro ao buscar horários disponíveis');
            console.error(error);
        }
    };

    // Função para criar novo horário de disponibilidade
    const createAvailability = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/availability-list-create/', newAvailability, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            setSuccess('Horário criado com sucesso!');
            setNewAvailability({ date: '', start_time: '', end_time: '' });
            fetchAvailabilities(); // Atualiza a lista de horários após criar um novo
        } catch (error) {
            setError('Erro ao criar horário');
            console.error(error);
        }
    };

    useEffect(() => {
        fetchAvailabilities();
    }, [navigate]);

    // Função para obter data e hora atuais no formato correto
    const getCurrentDateTime = () => {
        const now = new Date();
        const date = now.toISOString().split('T')[0]; // Formato YYYY-MM-DD
        const time = now.toTimeString().split(' ')[0].slice(0, 5); // Formato HH:MM
        return { date, time };
    };

    // Função para filtrar horários futuros
    const filterFutureAvailabilities = (availabilities) => {
        const { date: currentDate, time: currentTime } = getCurrentDateTime();

        return availabilities.filter((availability) => {
            if (availability.date > currentDate) {
                // Se a data do horário for maior que a data atual
                return true;
            } else if (availability.date === currentDate) {
                // Se a data do horário for hoje, verifica se o horário de início é maior que o horário atual
                return availability.start_time > currentTime;
            }
            return false;
        });
    };

    // Função para definir a data mínima (hoje)
    const getCurrentDate = () => {
        const today = new Date().toISOString().split('T')[0];
        return today;
    };

    // Função para definir a hora mínima (hora atual) se a data selecionada for o dia atual
    const getCurrentTime = () => {
        const now = new Date();
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        return `${hours}:${minutes}`;
    };

    // Verifica se a data selecionada é hoje para ajustar a hora mínima
    const handleDateChange = (e) => {
        const selectedDate = e.target.value;
        setNewAvailability({
            ...newAvailability,
            date: selectedDate
        });

        if (selectedDate === getCurrentDate()) {
            setMinTime(getCurrentTime()); // Se a data for hoje, define o mínimo de hora atual
        } else {
            setMinTime(''); // Se for outro dia, não há restrição de hora
        }
    };

    // Função para atualizar os valores de input
    const handleChange = (e) => {
        setNewAvailability({
            ...newAvailability,
            [e.target.name]: e.target.value
        });
    };

    return (
        <div className="availability-container">
            <Sidebar />
            <div className="main-content">
                <header className="header">
                    <h1>Gerenciar Horários de Disponibilidade</h1>
                </header>
                <div className="availability-form">
                    <h2>Criar Novo Horário</h2>
                    {error && <p className="error-message">{error}</p>}
                    {success && <p className="success-message">{success}</p>}
                    <form onSubmit={(e) => {
                        e.preventDefault();
                        createAvailability();
                    }}>
                        <label>
                            Data:
                            <input 
                                type="date" 
                                name="date"
                                min={getCurrentDate()} 
                                value={newAvailability.date}
                                onChange={handleDateChange}
                                required 
                            />
                        </label>
                        <label>
                            Início:
                            <input 
                                type="time" 
                                name="start_time" 
                                value={newAvailability.start_time}
                                min={minTime}
                                onChange={handleChange}
                                required 
                            />
                        </label>
                        <label>
                            Fim:
                            <input 
                                type="time" 
                                name="end_time" 
                                value={newAvailability.end_time}
                                onChange={handleChange}
                                required 
                            />
                        </label>
                        <button type="submit">Criar Horário</button>
                    </form>
                </div>
                <div className="availabilities-list">
                    <h2>Horários de Disponibilidade Futuros</h2>
                    {availabilities.length === 0 ? (
                        <p>Nenhum horário disponível</p>
                    ) : (
                        <ul>
                            {availabilities.map((availability, index) => (
                                <li key={index}>
                                    <p><strong>Data:</strong> {availability.date}</p>
                                    <p><strong>Hora:</strong> {availability.start_time} - {availability.end_time}</p>
                                </li>
                            ))}
                        </ul>
                    )}
                </div>
            </div>
        </div>
    );
};

export default AvailabilityManager;
