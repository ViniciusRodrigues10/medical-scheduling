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

function Menu ({userType}) {
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

    const menuItems = userType === 'paciente' ? [
        { path: '/patient/inicio', label: 'Início', icon: iconHome },
        { path: '/patient/medicos', label: 'Médicos', icon: iconDoctors },
        { path: '/patient/agenda', label: 'Agenda', icon: iconCalendar },
        { path: '/patient/historico-de-agendamentos', label: 'Histórico', icon: iconReports },
        { path: '/patient/perfil', label: 'Perfil', icon: iconSettings }
      ] : [
        { path: '/login', label: 'Início', icon: iconHome },
        { path: '/doctor/horarios', label: 'Horários', icon: iconDoctors },
        { path: '/doctor/agenda', label: 'Agenda', icon: iconCalendar },
        { path: '/doctor/historico', label: 'Histórico', icon: iconReports },
        { path: '/doctor/perfil', label: 'Perfil', icon: iconSettings }
      ];

    return (
        <div className="sidebar">
      <img src={logo} alt="Saúde Now" className="sidebar-logo" />
      <ul className="menu-list">
        {menuItems.map((item, index) => (
          <li
            key={index}
            className={`menu-item ${isActive(item.path) ? 'active' : ''}`}
            onClick={() => navigate(item.path)}
          >
            <img src={item.icon} alt={`Ícone de ${item.label}`} className="icon" />
            {item.label}
          </li>
        ))}
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
