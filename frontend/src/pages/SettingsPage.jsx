import React from 'react';
import { Volume2, VolumeX, Globe, Bell } from 'lucide-react';

const SettingsPage = ({ language, setLanguage }) => {
    const [voiceEnabled, setVoiceEnabled] = React.useState(true);
    const [notifications, setNotifications] = React.useState(true);

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Settings</h1>
                <p>Manage your preferences to personalize your experience.</p>
            </div>

            <div className="settings-grid">
                {/* Language Section */}
                <div className="settings-card">
                    <div className="s-icon"><Globe size={24} /></div>
                    <div className="s-content">
                        <h3>App Language</h3>
                        <p>Choose your preferred language for the interface.</p>
                        <div className="lang-switcher">
                            <button className={`l-btn ${language === 'en' ? 'active' : ''}`} onClick={() => setLanguage('en')}>English</button>
                            <button className={`l-btn ${language === 'hi' ? 'active' : ''}`} onClick={() => setLanguage('hi')}>हिंदी</button>
                            <button className={`l-btn ${language === 'mr' ? 'active' : ''}`} onClick={() => setLanguage('mr')}>मराठी</button>
                        </div>
                    </div>
                </div>

                {/* Voice Settings */}
                <div className="settings-card">
                    <div className="s-icon">
                        {voiceEnabled ? <Volume2 size={24} /> : <VolumeX size={24} />}
                    </div>
                    <div className="s-content">
                        <h3>Voice Responses</h3>
                        <p>Enable text-to-speech for chatbot responses.</p>
                        <label className="toggle-switch">
                            <input type="checkbox" checked={voiceEnabled} onChange={() => setVoiceEnabled(!voiceEnabled)} />
                            <span className="slider"></span>
                        </label>
                    </div>
                </div>

                {/* Notifications */}
                <div className="settings-card">
                    <div className="s-icon"><Bell size={24} /></div>
                    <div className="s-content">
                        <h3>Notifications</h3>
                        <p>Get alerts for policy renewals and updates.</p>
                        <label className="toggle-switch">
                            <input type="checkbox" checked={notifications} onChange={() => setNotifications(!notifications)} />
                            <span className="slider"></span>
                        </label>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SettingsPage;
