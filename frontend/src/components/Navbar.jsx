import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom'; // optimized import
import { ShieldCheck, Languages, Menu, X } from 'lucide-react';

const Navbar = ({ language, setLanguage }) => {
    const [showLanguageMenu, setShowLanguageMenu] = useState(false);
    const [showProfileMenu, setShowProfileMenu] = useState(false);
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
    const location = useLocation();

    // Close menus when clicking outside
    useEffect(() => {
        const handleClickOutside = () => {
            setShowLanguageMenu(false);
            setShowProfileMenu(false);
        };
        if (showLanguageMenu || showProfileMenu) document.addEventListener('click', handleClickOutside);
        return () => document.removeEventListener('click', handleClickOutside);
    }, [showLanguageMenu, showProfileMenu]);

    const selectLanguage = (lang, e) => {
        e.stopPropagation();
        setLanguage(lang);
        setShowLanguageMenu(false);
    };

    const navLinks = {
        en: [
            { name: 'Home', path: '/' },
            { name: 'Chat', path: '/chat' },
            { name: 'Learn', path: '/education' },
            { name: 'Dashboard', path: '/dashboard' },
            { name: 'Support', path: '/support' },
        ],
        hi: [
            { name: 'होम', path: '/' },
            { name: 'चैट', path: '/chat' },
            { name: 'सीखें', path: '/education' },
            { name: 'डैशबोर्ड', path: '/dashboard' },
            { name: 'सहायता', path: '/support' },
        ],
        mr: [
            { name: 'होम', path: '/' },
            { name: 'चॅट', path: '/chat' },
            { name: 'शिका', path: '/education' },
            { name: 'डॅशबोर्ड', path: '/dashboard' },
            { name: 'मदत', path: '/support' },
        ]
    };

    const currentLinks = navLinks[language] || navLinks.en;

    return (
        <nav className="header">
            <Link to="/" className="brand" style={{ textDecoration: 'none' }}>
                <div className="brand-logo">
                    <ShieldCheck size={24} />
                </div>
                <div className="brand-text">
                    <h1>
                        {language === 'en' && 'Suraksha Sahayak'}
                        {language === 'hi' && 'सुरक्षा सहायक'}
                        {language === 'mr' && 'सुरक्षा सहाय्यक'}
                    </h1>
                    <p className="mobile-hidden">
                        {language === 'en' && 'Your Trusted Insurance Advisor'}
                        {language === 'hi' && 'आपका विश्वसनीय बीमा सलाहकार'}
                        {language === 'mr' && 'तुमचा विश्वसनीय विमा सल्लागार'}
                    </p>
                </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="desktop-nav">
                {currentLinks.map(link => (
                    <Link
                        key={link.path}
                        to={link.path}
                        className={`nav-link ${location.pathname === link.path ? 'active' : ''}`}
                    >
                        {link.name}
                    </Link>
                ))}
            </div>

            <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
                {/* Language Toggle */}
                <div style={{ position: 'relative' }} onClick={(e) => e.stopPropagation()}>
                    <button
                        className={`action-btn ${showLanguageMenu ? 'active' : ''}`}
                        onClick={() => setShowLanguageMenu(!showLanguageMenu)}
                        title="Change Language"
                    >
                        <Languages size={20} />
                        <span style={{ marginLeft: '5px', fontSize: '0.9rem', fontWeight: 600 }}>
                            {language.toUpperCase()}
                        </span>
                    </button>

                    {showLanguageMenu && (
                        <div className="language-dropdown">
                            <div className={`lang-option ${language === 'en' ? 'selected' : ''}`} onClick={(e) => selectLanguage('en', e)}>English</div>
                            <div className={`lang-option ${language === 'hi' ? 'selected' : ''}`} onClick={(e) => selectLanguage('hi', e)}>हिंदी</div>
                            <div className={`lang-option ${language === 'mr' ? 'selected' : ''}`} onClick={(e) => selectLanguage('mr', e)}>मराठी</div>
                        </div>
                    )}
                </div>

                {/* Profile Toggle */}
                <div style={{ position: 'relative' }} onClick={(e) => e.stopPropagation()}>
                    <button
                        className="action-btn"
                        title="Profile"
                        onClick={() => setShowProfileMenu(!showProfileMenu)}
                    >
                        <div className="avatar" style={{ width: 28, height: 28, fontSize: '0.8rem' }}>👤</div>
                    </button>

                    {showProfileMenu && (
                        <div className="language-dropdown" style={{ width: '200px' }}>
                            <div className="menu-header" style={{ padding: '1rem', borderBottom: '1px solid #e2e8f0' }}>
                                <strong>User Profile</strong>
                                <div style={{ fontSize: '0.8rem', color: '#64748b' }}>user@example.com</div>
                            </div>
                            <Link to="/details" className="lang-option" onClick={() => setShowProfileMenu(false)}>My Profile</Link>
                            <Link to="/documents" className="lang-option" onClick={() => setShowProfileMenu(false)}>Documents Vault</Link>
                            <Link to="/roadmap" className="lang-option" onClick={() => setShowProfileMenu(false)}>Insurance Roadmap</Link>
                            <Link to="/settings" className="lang-option" onClick={() => setShowProfileMenu(false)}>Settings</Link>
                            <div style={{ borderTop: '1px solid #e2e8f0', marginTop: '0.5rem' }}>
                                <Link to="/login" className="lang-option" style={{ color: '#dc2626' }} onClick={() => setShowProfileMenu(false)}>Logout</Link>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
