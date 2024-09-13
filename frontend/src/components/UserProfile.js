import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Sidebar from './Menu';
import '../_assets/css/userProfile.css';

const UserProfile = () => {
    const [userData, setUserData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState('');
    const [formData, setFormData] = useState({
        email: '',
        password: '',
        first_name: '',
        last_name: '',
        gender: 1,
        new_password: ''
    });
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
                setFormData({
                    email: response.data.user_info.email,
                    password: '',
                    first_name: response.data.user_info.first_name,
                    last_name: response.data.user_info.last_name,
                    gender: response.data.user_info.gender,
                    new_password: ''
                });
                setLoading(false);
            } catch (error) {
                setError('Erro ao obter dados do usuário');
                console.error(error);
                setLoading(false);
            }
        };

        fetchUserData();
    }, [navigate]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
    };

    const handleUpdate = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        const dataToSend = { ...formData };
        if (!dataToSend.new_password) {
            delete dataToSend.new_password;
        }

        try {
            await axios.put('http://127.0.0.1:8000/api/update-user/', dataToSend, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            alert('Dados atualizados com sucesso!');
        } catch (error) {
            setError('Erro ao atualizar dados do usuário');
            console.error(error);
        }
    };

    const handleDeleteAccount = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            await axios.delete('http://127.0.0.1:8000/api/delete-account/', {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            alert('Conta excluída com sucesso!');
            navigate('/login');
        } catch (error) {
            setError('Erro ao excluir conta');
            console.error(error);
        }
    };

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
                            <button onClick={() => navigate('/historico-medico')} className="history-button">Preencher Histórico Médico</button>
                            <div className="user-card">
                                <form onSubmit={handleUpdate}>
                                    <h3>Redefinir Dados</h3>
                                    <div className="form-group">
                                        <label htmlFor="first_name">Nome:</label>
                                        <input
                                            type="text"
                                            id="first_name"
                                            name="first_name"
                                            value={formData.first_name}
                                            onChange={handleInputChange}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="last_name">Sobrenome:</label>
                                        <input
                                            type="text"
                                            id="last_name"
                                            name="last_name"
                                            value={formData.last_name}
                                            onChange={handleInputChange}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="email">Email:</label>
                                        <input
                                            type="email"
                                            id="email"
                                            name="email"
                                            value={formData.email}
                                            onChange={handleInputChange}
                                        />
                                    </div>
                                    <div className="form-group">
                                        <label htmlFor="gender">Gênero:</label>
                                        <select
                                            id="gender"
                                            name="gender"
                                            value={formData.gender}
                                            onChange={handleInputChange}
                                        >
                                            <option value={1}>Masculino</option>
                                            <option value={2}>Feminino</option>
                                            <option value={3}>Outro</option>
                                        </select>
                                    </div>
                                    <div className="form-group">
                                        <button type="submit" className="update-button">Atualizar Dados</button>
                                    </div>
                                </form>
                            </div>
                            <div className="user-card">
                                <h3>Redefinir Senha</h3>
                                <div className="form-group">
                                    <label htmlFor="password">Senha Atual:</label>
                                    <input
                                        type="password"
                                        id="password"
                                        name="password"
                                        value={formData.password}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="new_password">Nova Senha:</label>
                                    <input
                                        type="password"
                                        id="new_password"
                                        name="new_password"
                                        value={formData.new_password}
                                        onChange={handleInputChange}
                                    />
                                </div>
                                <div className="form-group">
                                    <button type="submit" className="update-button">Atualizar Senha</button>
                                </div>
                            </div>
                            <div className="delete-section">
                                <h3>Excluir Conta</h3>
                                <button onClick={handleDeleteAccount} className="delete-profile-button">Excluir Conta</button>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
