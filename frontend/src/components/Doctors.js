import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Sidebar from './Menu';
import '../_assets/css/doctors.css';

const DoctorList = () => {
    const [doctors, setDoctors] = useState([]);
    const [filteredDoctors, setFilteredDoctors] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('token');
                if (!token) {
                    window.location.href = '/login';
                    return;
                }

                const response = await axios.get('http://localhost:8000/api/doctor-informations/', {
                    headers: {
                        'Authorization': `Token ${token}`
                    }
                });
                setDoctors(response.data);
                setFilteredDoctors(response.data);
            } catch (err) {
                setError('Erro ao carregar dados dos médicos');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const handleSearch = (event) => {
        const term = event.target.value.toLowerCase();
        setSearchTerm(term);
        if (term) {
            const filtered = doctors.filter(doctor =>
                `${doctor.first_name} ${doctor.last_name}`.toLowerCase().includes(term)
            );
            setFilteredDoctors(filtered);
        } else {
            setFilteredDoctors(doctors);
        }
    };

    if (loading) {
        return <div className="loading">Carregando...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="doctor-list-container">
            <Sidebar />
            <div className="main-content">
                <header className="doctor-list-header">
                    <h1>Lista de Médicos</h1>
                </header>
                <input
                    type="text"
                    placeholder="Pesquisar pelo nome do médico"
                    value={searchTerm}
                    onChange={handleSearch}
                    className="search-bar"
                />
                <div className="doctor-list-content">
                    {filteredDoctors.map((doctor) => (
                        <div key={doctor.user} className="doctor-card">
                            <h2>Dr. {doctor.first_name} {doctor.last_name}</h2>
                            <p><strong>Especialidade:</strong> {doctor.specialty}</p>
                            <p><strong>CRM:</strong> {doctor.crm}</p>
                            <p><strong>Biografia:</strong> {doctor.biography}</p>
                            <p><strong>Telefone:</strong> {doctor.telephone}</p>
                            <p><strong>Data de Nascimento:</strong> {doctor.date_of_birth}</p>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default DoctorList;
