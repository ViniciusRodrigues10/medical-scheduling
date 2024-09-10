import React from 'react';
import { useNavigate } from 'react-router-dom';
import '../_assets/css/menu.css'; // Importando o CSS

// Importando as imagens corretamente
import logo from '../_assets/img/logo.png';
import iconHome from '../_assets/img/icone-casa.png';
import iconDoctors from '../_assets/img/icone-perfil.png';
import iconCalendar from '../_assets/img/icone-agenda.png';
import iconReports from '../_assets/img/icone-estati.png';
import iconSettings from '../_assets/img/icone-opcao.png';

const Menu = () => {
    const navigate = useNavigate(); // Inicializa o hook de navegação
  
    return (
        <div className="sidebar">
            <img src={logo} alt="Saúde Now" className="sidebar-logo" />
            <ul className="menu-list">
                <li className="menu-item" onClick={() => navigate('/home')}>
                    <img src={iconHome} alt="Ícone de Início" className="icon" />
                    Início
                </li>
                <li className="menu-item" onClick={() => navigate('/medicos')}>
                    <img src={iconDoctors} alt="Ícone de Médicos" className="icon" />
                    Médicos
                </li>
                <li className="menu-item" onClick={() => navigate('/agenda')}>
                    <img src={iconCalendar} alt="Ícone de Agenda" className="icon" />
                    Agenda
                </li>
                <li className="menu-item" onClick={() => navigate('/relatorios')}>
                    <img src={iconReports} alt="Ícone de Relatórios" className="icon" />
                    Relatórios
                </li>
                <li className="menu-item" onClick={() => navigate('/opcoes')}>
                    <img src={iconSettings} alt="Ícone de Opções" className="icon" />
                    Opções
                </li>
            </ul>
            <button onClick={() => navigate('/login')} className="logout-button">Sair</button>
        </div>
    );
};

export default Menu;
