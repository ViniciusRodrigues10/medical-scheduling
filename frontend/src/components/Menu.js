import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../_assets/css/menu.css'; 
import logo from '../_assets/img/logo.png';
import iconHome from '../_assets/img/icone-casa.png';
import iconDoctors from '../_assets/img/icone-perfil.png';
import iconCalendar from '../_assets/img/icone-agenda.png';
import iconReports from '../_assets/img/icone-estati.png';
import iconSettings from '../_assets/img/icone-opcao.png';

const Menu = () => {
    const navigate = useNavigate();
    const location = useLocation(); // Hook para obter a localização atual

    // Função para determinar se o item do menu está ativo
    const isActive = (path) => location.pathname === path;

    return (
        <div className="sidebar">
            <img src={logo} alt="Saúde Now" className="sidebar-logo" />
            <ul className="menu-list">
                <li className={`menu-item ${isActive('/login') ? 'active' : ''}`} onClick={() => navigate('/login')}>
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
            <button onClick={() => navigate('/login')} className="logout-button">Sair</button>
        </div>
    );
};

export default Menu;
