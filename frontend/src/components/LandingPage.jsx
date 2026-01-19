import React from 'react';
import { ArrowRight, ShieldCheck, Zap, Users, MessageSquare, FileCheck, Globe, FileText } from 'lucide-react';
import { Link } from 'react-router-dom';

const LandingPage = ({ onStartChat, language }) => {
    const content = {
        en: {
            badge: "AI-Powered Insurance Advisor",
            titleStart: "Secure Your Future",
            titleEnd: "Smart Advice",
            with: "with",
            subtitle: "Get personalized insurance plans, multilingual support, and instant roadmaps — all in one conversation.",
            cta: "Start Consultation",
            features: [
                { title: "Conversational AI", desc: "Chat naturally in your preferred language to get instant answers." },
                { title: "Multilingual Support", desc: "We speak English, Hindi, Marathi, and more. No barriers." },
                { title: "Personalized Roadmap", desc: "Receive a comprehensive PDF plan tailored to your life stage." }
            ]
        },
        hi: {
            badge: "AI-संचालित बीमा सलाहकार",
            titleStart: "अपने भविष्य को सुरक्षित करें",
            titleEnd: "स्मार्ट सलाह",
            with: "के साथ",
            subtitle: "व्यक्तिगत बीमा योजनाएं, बहुभाषी समर्थन और त्वरित रोडमैप प्राप्त करें - सब कुछ एक ही बातचीत में।",
            cta: "परामर्श शुरू करें",
            features: [
                { title: "संवादी AI", desc: "त्वरित उत्तर पाने के लिए अपनी पसंदीदा भाषा में स्वाभाविक रूप से चैट करें।" },
                { title: "बहुभाषी समर्थन", desc: "हम अंग्रेजी, हिंदी, मराठी और बहुत कुछ बोलते हैं। कोई बाधा नहीं।" },
                { title: "व्यक्तिगत रोडमैप", desc: "अपने जीवन के चरण के अनुरूप एक व्यापक PDF योजना प्राप्त करें।" }
            ]
        },
        mr: {
            badge: "AI-आधारित विमा सल्लागार",
            titleStart: "आपले भविष्य सुरक्षित करा",
            titleEnd: "स्मार्ट सल्ल्या",
            with: "सह",
            subtitle: "वैयक्तिक विमा योजना, बहुभाषिक समर्थन आणि त्वरित रोडमॅप मिळवा - सर्व काही एकाच संभाषणात.",
            cta: "सल्लामसलत सुरू करा",
            features: [
                { title: "संवादी AI", desc: "त्वरित उत्तरे मिळवण्यासाठी आपल्या पसंतीच्या भाषेत नैसर्गिकरित्या चॅट करा." },
                { title: "बहुभाषिक समर्थन", desc: "आम्ही इंग्रजी, हिंदी, मराठी आणि बरेच काही बोलतो. कोणताही अडथळा नाही." },
                { title: "वैयक्तिक रोडमॅप", desc: "तुमच्या जीवनाच्या टप्प्याला अनुसरून एक व्यापक PDF योजना मिळवा." }
            ]
        }
    };

    const t = content[language] || content.en;

    return (
        <div className="landing-page">
            {/* Hero Section */}
            <section className="hero-section">
                <div className="hero-content">
                    <h1>
                        {language === 'en' && 'Bridging the Insurance Gap for Rural India'}
                        {language === 'hi' && 'ग्रामीण भारत के लिए बीमा की खाई को पाटना'}
                        {language === 'mr' && 'ग्रामीण भारतासाठी विम्याची दरी कमी करणे'}
                    </h1>
                    <p>
                        {language === 'en' && 'Empowering communities with simplified education, AI guidance, and easy access to schemes.'}
                        {language === 'hi' && 'सरल शिक्षा, एआई मार्गदर्शन और योजनाओं तक आसान पहुंच के साथ समुदायों को सशक्त बनाना।'}
                        {language === 'mr' && 'सरलीकृत शिक्षण, एआय मार्गदर्शन आणि योजनांमध्ये सुलभ प्रवेशासह समुदायांना सक्षम करणे.'}
                    </p>

                    <div className="trust-badges-hero">
                        <span className="t-badge"><ShieldCheck size={18} /> Smart Analysis</span>
                        <span className="t-badge"><Users size={18} /> Community Trust</span>
                        <span className="t-badge"><FileCheck size={18} /> Easy Guidance</span>
                    </div>

                    <div className="cta-group">
                        <button className="cta-button primary" onClick={onStartChat}>
                            {language === 'en' && 'Check Eligibility'}
                            {language === 'hi' && 'पात्रता जांचें'}
                            {language === 'mr' && 'पात्रता तपासा'}
                            <ArrowRight size={20} />
                        </button>
                        <Link to="/education" className="cta-button secondary">
                            {language === 'en' && 'View Schemes'}
                            {language === 'hi' && 'योजनाएं देखें'}
                            {language === 'mr' && 'योजना पहा'}
                        </Link>
                    </div>
                </div>
            </section>
            <div className="features-grid">
                <div className="feature-card">
                    <div className="feature-icon"><MessageSquare size={24} /></div>
                    <h3>{t.features[0].title}</h3>
                    <p>{t.features[0].desc}</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon"><Globe size={24} /></div>
                    <h3>{t.features[1].title}</h3>
                    <p>{t.features[1].desc}</p>
                </div>
                <div className="feature-card">
                    <div className="feature-icon"><FileText size={24} /></div>
                    <h3>{t.features[2].title}</h3>
                    <p>{t.features[2].desc}</p>
                </div>
            </div>
        </div>
    );
};

export default LandingPage;
