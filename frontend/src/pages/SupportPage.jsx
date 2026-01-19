import React, { useState } from 'react';
import { HelpCircle, Phone, Mail, MessageCircle, ChevronDown, ChevronUp } from 'lucide-react';
import { Link } from 'react-router-dom';

const SupportPage = () => {

    const faqs = [
        {
            q: "How do I claim insurance?",
            a: "You can file a claim instantly through our chatbot or call our toll-free number 1800-123-456."
        },
        {
            q: "Can I upgrade my plan later?",
            a: "Yes, you can upgrade your plan during the renewal period or by contacting support."
        },
        {
            q: "Is PMFBY available for all crops?",
            a: "PMFBY covers notified crops in notified areas. Please check the active list in the Education Hub."
        },
        {
            q: "What documents are needed for KYC?",
            a: "Aadhar Card, PAN Card, and a recent photograph are mandatory for KYC completion."
        }
    ];

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Help & Support</h1>
                <p>We are here to assist you 24/7</p>
            </div>

            <div className="support-grid">
                {/* Contact Cards */}
                <div className="contact-section">
                    <div className="contact-card">
                        <div className="icon-box"><Phone size={24} /></div>
                        <h3>Call Us</h3>
                        <p>1800-123-456</p>
                    </div>
                    <div className="contact-card">
                        <div className="icon-box"><Mail size={24} /></div>
                        <h3>Email</h3>
                        <p>support@suraksha.com</p>
                    </div>
                    <Link to="/chat" className="contact-card">
                        <div className="icon-box"><MessageCircle size={24} /></div>
                        <h3>Chat with AI</h3>
                        <p>Instant Answers</p>
                    </Link>
                </div>

                {/* FAQs */}
                <div className="faq-section">
                    <h2>Frequently Asked Questions</h2>
                    <div className="faq-list">
                        {faqs.map((faq, index) => (
                            <FAQItem key={index} faq={faq} />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

const FAQItem = ({ faq }) => {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <div className={`faq-item ${isOpen ? 'open' : ''}`} onClick={() => setIsOpen(!isOpen)}>
            <div className="faq-question">
                <span>{faq.q}</span>
                {isOpen ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
            </div>
            {isOpen && <div className="faq-answer">{faq.a}</div>}
        </div>
    );
}

export default SupportPage;
