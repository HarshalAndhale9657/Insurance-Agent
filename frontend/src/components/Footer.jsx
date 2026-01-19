import React from 'react';
import { ShieldCheck, Facebook, Twitter, Instagram, Mail, Phone } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="site-footer">
            <div className="footer-content compact">

                {/* Brand Section */}
                <div className="footer-brand">
                    <div className="f-logo">
                        <ShieldCheck size={24} />
                        <span>Suraksha Sahayak</span>
                    </div>
                </div>

                {/* Contact Info Compact */}
                <div className="footer-contact-compact">
                    <div className="contact-item">
                        <Phone size={16} /> <span>1800-123-9999</span>
                    </div>
                    <div className="contact-item">
                        <Mail size={16} /> <span>help@suraksha.gov.in</span>
                    </div>
                    <div className="social-icons-compact">
                        <a href="#" className="s-link"><Facebook size={18} /></a>
                        <a href="#" className="s-link"><Twitter size={18} /></a>
                        <a href="#" className="s-link"><Instagram size={18} /></a>
                    </div>
                </div>
            </div>

            <div className="footer-bottom compact">
                <p>&copy; 2024 Suraksha Sahayak. All Rights Reserved.</p>
            </div>
        </footer>
    );
};

export default Footer;
