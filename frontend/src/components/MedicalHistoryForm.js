import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../_assets/css/medicalHistoryForm.css';

const MedicalHistoryFormPage = () => {
  const [currentMedications, setCurrentMedications] = useState('');
  const [allergies, setAllergies] = useState('');
  const [surgeries, setSurgeries] = useState('');
  const [familyHistory, setFamilyHistory] = useState('');
  const [bloodType, setBloodType] = useState('');
  const [healthPlan, setHealthPlan] = useState('');
  const [emergencyContacts, setEmergencyContacts] = useState([
    { name: '', phone_number: '' },
    { name: '', phone_number: '' },
  ]);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleContactChange = (index, field, value) => {
    const newContacts = [...emergencyContacts];
    newContacts[index][field] = value;
    setEmergencyContacts(newContacts);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    const medicalHistoryData = {
      current_medications: currentMedications,
      allergies: allergies,
      surgeries: surgeries,
      family_history: familyHistory,
      blood_type: bloodType,
      health_plan: healthPlan,
      emergency_contacts: emergencyContacts,
    };

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post('http://127.0.0.1:8000/api/medical-history/', medicalHistoryData, {
        headers: {
          'Authorization': `Token ${token}`,
          'Content-Type': 'application/json',
        },
      });
      if (response.status === 201) {
        navigate('/patient/perfil'); // Navega de volta para a página de perfil do usuário após a submissão
      }
    } catch (error) {
      setError('Erro ao enviar dados. Por favor, tente novamente.');
      console.error(error);
    }
  };

  return (
    <div className="form-page">
      <div className="form-container">
        <h2>Histórico Médico</h2>
        {error && <p className="error">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Medicações Atuais:</label>
            <textarea
              value={currentMedications}
              onChange={(e) => setCurrentMedications(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Alergias:</label>
            <textarea
              value={allergies}
              onChange={(e) => setAllergies(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Cirurgias:</label>
            <textarea
              value={surgeries}
              onChange={(e) => setSurgeries(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Histórico Familiar:</label>
            <textarea
              value={familyHistory}
              onChange={(e) => setFamilyHistory(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Tipo Sanguíneo:</label>
            <input
              type="text"
              value={bloodType}
              onChange={(e) => setBloodType(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>Plano de Saude:</label>
            <input
              type="text"
              value={healthPlan}
              onChange={(e) => setHealthPlan(e.target.value)}
              required
            />
          </div>
          <h3>Contatos de Emergência:</h3>
          {emergencyContacts.map((contact, index) => (
            <div key={index} className="form-group">
              <label>Nome:</label>
              <input
                type="text"
                value={contact.name}
                onChange={(e) => handleContactChange(index, 'name', e.target.value)}
                required
              />
              <label>Telefone:</label>
              <input
                type="text"
                value={contact.phone_number}
                onChange={(e) => handleContactChange(index, 'phone_number', e.target.value)}
                required
              />
            </div>
          ))}
          <button type="submit">Salvar Histórico Médico</button>
        </form>
      </div>
    </div>
  );
};

export default MedicalHistoryFormPage;