import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';
import LandingPage from './components/LandingPage';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import AuthPage from './pages/AuthPage';
import EducationPage from './pages/EducationPage';
import DashboardPage from './pages/DashboardPage';
import ComparePage from './pages/ComparePage';
import PurchasePage from './pages/PurchasePage';
import SupportPage from './pages/SupportPage';
import DocumentsPage from './pages/DocumentsPage';
import RoadmapPage from './pages/RoadmapPage';
import SettingsPage from './pages/SettingsPage';
import ProfilePage from './pages/ProfilePage';

const MainApp = () => {
  const [language, setLanguage] = useState('en'); // 'en', 'hi', 'mr'
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const navigate = useNavigate();

  return (
    <div className="app-container">
      <Navbar language={language} setLanguage={setLanguage} />

      <Routes>
        <Route
          path="/"
          element={
            <LandingPage
              language={language}
              onStartChat={() => navigate('/chat')}
            />
          }
        />
        <Route
          path="/chat"
          element={<ChatInterface language={language} voiceEnabled={voiceEnabled} />}
        />
        <Route path="/login" element={<AuthPage />} />
        <Route path="/education" element={<EducationPage language={language} />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/compare" element={<ComparePage />} />
        <Route path="/purchase" element={<PurchasePage />} />
        <Route path="/support" element={<SupportPage />} />
        <Route path="/documents" element={<DocumentsPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
        <Route path="/settings" element={<SettingsPage language={language} setLanguage={setLanguage} voiceEnabled={voiceEnabled} setVoiceEnabled={setVoiceEnabled} />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Routes>
      <Footer />
    </div>
  );
};

function App() {
  return (
    <Router>
      <MainApp />
    </Router>
  );
}

export default App;
