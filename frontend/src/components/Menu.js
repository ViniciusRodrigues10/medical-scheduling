import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import axios from 'axios';
import Modal from 'react-modal';  
import '../_assets/css/menu.css'; 
import logo from '../_assets/img/logo.png';
import iconHome from '../_assets/img/icone-casa.png';
import iconDoctors from '../_assets/img/icone-perfil.png';
import iconCalendar from '../_assets/img/icone-agenda.png';
import iconReports from '../_assets/img/icone-estati.png';
import iconSettings from '../_assets/img/icone-opcao.png';


Modal.setAppElement('#root');

const Menu = () => {
    const navigate = useNavigate();
    const location = useLocation(); 
    const [modalIsOpen, setModalIsOpen] = useState(false);  

    const isActive = (path) => location.pathname === path;

    const handleLogout = async () => {
        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        try {
            await axios.post('http://127.0.0.1:8000/api/logout/', {}, {
                headers: {
                    'Authorization': `Token ${token}`
                }
            });
            localStorage.removeItem('token');
            navigate('/login');
        } catch (error) {
            console.error('Erro ao fazer logout:', error);
        }
    };

    const openModal = () => {
        setModalIsOpen(true);
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    return (
        <div className="sidebar">
            <img src={logo} alt="Saúde Now" className="sidebar-logo" />
            <ul className="menu-list">
                <li className={`menu-item ${isActive('/login/inicio') ? 'active' : ''}`} onClick={() => navigate('/login/inicio')}>
                    <img src={iconHome} alt="Ícone de Início" className="icon" />
                    Início
                </li>
                <li className={`menu-item ${isActive('/medicos') ? 'active' : ''}`} onClick={() => navigate('/medicos')}>
                    <img src={iconDoctors} alt="Ícone de Médicos" className="icon" />
                    Médicos
                </li>
                <li className={`menu-item ${isActive('/agenda') ? 'active' : ''}`} onClick={() => navigate('/agenda')}>
                    <img src={iconCalendar} alt="Ícone de Agenda" className="icon" />
                    Agenda
                </li>
                <li className={`menu-item ${isActive('/login/historico-de-agendamentos') ? 'active' : ''}`} onClick={() => navigate('/login/historico-de-agendamentos')}>
                    <img src={iconReports} alt="Ícone de Relatórios" className="icon" />
                    Histórico
                </li>
                <li className={`menu-item ${isActive('/perfil') ? 'active' : ''}`} onClick={() => navigate('/perfil')}>
                    <img src={iconSettings} alt="Ícone de Opções" className="icon" />
                    Perfil
                </li>
            </ul>
            <button onClick={openModal} className="logout-button">Sair</button>

            <Modal
                isOpen={modalIsOpen}
                onRequestClose={closeModal}
                contentLabel="Confirmação de Logout"
                className="modal"
                overlayClassName="overlay"
            >
                <h2>Tem certeza que deseja sair?</h2>
                <button onClick={handleLogout} className="confirm-button">Sim</button>
                <button onClick={closeModal} className="cancel-button">Não</button>
            </Modal>
        </div>
    );
};

export default Menu;
