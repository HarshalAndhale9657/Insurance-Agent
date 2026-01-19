import React, { useState } from 'react';
import { Heart, Umbrella, Tractor, Car, PlayCircle, BookOpen } from 'lucide-react';

const EducationPage = ({ language = 'en' }) => {
    const [playingTopic, setPlayingTopic] = useState(null);
    const [audioUrl, setAudioUrl] = useState(null);
    const [loading, setLoading] = useState(false);
    const [audioElement, setAudioElement] = useState(null);
    const [expandedTopic, setExpandedTopic] = useState(null);

    // Safety check for language
    const currentLang = ['en', 'hi', 'mr'].includes(language) ? language : 'en';

    const topics = [
        {
            id: 1,
            title: 'Health Insurance',
            desc: 'Protect your family from medical emergencies. Covers hospitalization, medicines, and more.',
            icon: <Heart size={32} />,
            color: '#ef4444' // red
        },
        {
            id: 2,
            title: 'Life Insurance',
            desc: 'Secure your family\'s future. Get life cover and savings benefits.',
            icon: <Umbrella size={32} />,
            color: '#3b82f6' // blue
        },
        {
            id: 3,
            title: 'Crop Insurance',
            desc: 'PMFBY scheme details. Protect crops against natural calamities.',
            icon: <Tractor size={32} />,
            color: '#22c55e' // green
        },
        {
            id: 4,
            title: 'Vehicle Insurance',
            desc: 'Mandatory third-party liability and damage protection for your vehicle.',
            icon: <Car size={32} />,
            color: '#f59e0b' // amber
        }
    ];

    const content = {
        'Health Insurance': {
            en: "Health insurance covers medical costs such as hospitalization, medicines, and doctor fees. Key schemes include Ayushman Bharat for free treatment up to 5 Lakhs.",
            detailed_en: "Health insurance is a contract where an insurer pays for your medical expenses in exchange for a premium. \n\n**Key Benefits:**\n• **Cashless Treatment:** Get treated at network hospitals without paying upfront.\n• **Ayushman Bharat (PM-JAY):** Provides ₹5 Lakh coverage per family per year for secondary and tertiary care hospitalization.\n• **Critical Illness Cover:** Lump sum payout for serious diseases like cancer or heart attack.\n• **Tax Benefits:** Under Section 80D, you can save tax on premiums paid.\n\n**Why you need it:** Rising medical inflation means a single hospitalization can wipe out your savings. Health insurance ensures you get the best care without financial stress.",
            hi: "स्वास्थ्य बीमा अस्पताल, दवा और डॉक्टर की फीस जैसी चिकित्सा लागतों को कवर करता है। मुख्य योजनाओं में 5 लाख तक के मुफ्त इलाज के लिए आयुष्मान भारत शामिल है।",
            mr: "आरोग्य विमा हॉस्पिटलायझेशन, औषधे आणि डॉक्टरांची फी यासारख्या वैद्यकीय खर्चाचा समावेश करतो. प्रमुख योजनांमध्ये 5 लाखांपर्यंत मोफत उपचारांसाठी आयुष्मान भारतचा समावेश आहे."
        },
        'Life Insurance': {
            en: "Life insurance provides financial security to your family in case of untimely death. Term plans like PMJJBY offer coverage of 2 Lakhs for just ₹436/year.",
            detailed_en: "Life insurance ensures your family's financial stability in your absence.\n\n**Types of Life Insurance:**\n• **Term Insurance:** Pure protection plan. High cover at low premium.\n• **PMJJBY (Pradhan Mantri Jeevan Jyoti Bima Yojana):** A government-backed term plan offering ₹2 Lakh life cover for just ₹436/year. Available for ages 18-50.\n• **Endowment Plans:** Combine insurance with savings.\n\n**Why it matters:** It acts as an income replacement tool, helping your dependents pay off debts, fund education, and maintain their lifestyle.",
            hi: "जीवन बीमा असामयिक मृत्यु के मामले में आपके परिवार को वित्तीय सुरक्षा प्रदान करता है। पीएमजेजेबीवाई जैसी टर्म योजनाएं सिर्फ ₹436/वर्ष में 2 लाख का कवर देती हैं।",
            mr: "जीवन विमा अकाली मृत्यूच्या प्रसंगी आपल्या कुटुंबाला आर्थिक सुरक्षा प्रदान करतो. पीएमजेजेबीवाई सारख्या टर्म प्लॅन फक्त ₹436/वर्षात 2 लाखांचे संरक्षण देतात."
        },
        'Crop Insurance': {
            en: "PMFBY protects farmers against crop loss due to natural calamities like drought or flood. Premium is very low (2% for Kharif, 1.5% for Rabi).",
            detailed_en: "Pradhan Mantri Fasal Bima Yojana (PMFBY) is the flagship crop insurance scheme of India.\n\n**Coverage:**\n• Prevents sowing/planting risks.\n• Standing crop loss due to non-preventable risks like drought, flood, dry spells, and pests.\n• Post-harvest losses for crops kept in field to dry up to 14 days.\n\n**Premium Rates:**\n• Kharif Crops: 2% of Sum Insured.\n• Rabi Crops: 1.5% of Sum Insured.\n• Commercial/Horticulture Crops: 5%.\n\n**How to Apply:** Visit your nearest bank branch, CSC center, or the PMFBY portal.",
            hi: "पीएमएफबीवाई सूखा या बाढ़ जैसी प्राकृतिक आपदाओं के कारण फसल के नुकसान से किसानों की रक्षा करती है। प्रीमियम बहुत कम है (खरीफ के लिए 2%, रबी के लिए 1.5%)।",
            mr: "पीएमएफबीवाई दुष्काळ किंवा पूर यासारख्या नैसर्गिक आपत्तींमुळे पिकाच्या नुकसानीपासून शेतकऱ्यांचे संरक्षण करते. प्रीमियम खूप कमी आहे (खरीपसाठी 2%, रब्बीसाठी 1.5%)."
        },
        'Vehicle Insurance': {
            en: "Motor insurance is mandatory by law. Third-party liability covers damages to others, while comprehensive covers your own vehicle damage too.",
            detailed_en: "Motor insurance provides protection against accidents, theft, and third-party liabilities.\n\n**Mandatory Requirement:** The Motor Vehicles Act makes 'Third-Party Liability' insurance compulsory for all vehicles in India. It covers damages/injuries caused to others by your vehicle.\n\n**Comprehensive Policy:** Covers your own vehicle damages due to accidents, fire, theft, or natural calamities. \n\n**Add-ons:** Zero Depreciation, Roadside Assistance, and Engine Protection can enhance your coverage.",
            hi: "मोटर बीमा कानूनन अनिवार्य है। थर्ड-पार्टी लायबिलिटी दूसरों को होने वाले नुकसान को कवर करती है, जबकि व्यापक बीमा आपके वाहन के नुकसान को भी कवर करता है।",
            mr: "वाहन विमा कायद्याने अनिवार्य आहे. थर्ड-पार्टी लायबिलिटी इतरांचे नुकसान भरून काढते, तर सर्वसमावेशक विमा तुमच्या वाहनाचे नुकसान देखील भरून काढतो."
        }
    };

    const handleListen = async (topic) => {
        if (playingTopic === topic.title && audioUrl) {
            audioElement.pause();
            setPlayingTopic(null);
            return;
        }

        setLoading(true);
        setPlayingTopic(topic.title);

        try {
            const topicContent = content[topic.title];
            const textToSpeak = topicContent?.[currentLang] || topicContent?.['en'];

            if (!textToSpeak) throw new Error("No text content found for this topic.");

            const response = await fetch('http://localhost:8000/api/tts', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    text: textToSpeak,
                    language: currentLang
                })
            });

            if (response.ok) {
                const data = await response.json();

                if (data.audio_url) {
                    setAudioUrl(data.audio_url);

                    if (audioElement) audioElement.pause();
                    const newAudio = new Audio(data.audio_url);
                    newAudio.play();
                    newAudio.onended = () => setPlayingTopic(null);
                    setAudioElement(newAudio);
                } else {
                    throw new Error("No audio URL received");
                }
            } else {
                console.error("TTS Failed");
                alert("Audio generation failed. Please try again.");
                setPlayingTopic(null);
            }
        } catch (error) {
            console.error("Error playing audio:", error);
            setPlayingTopic(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Insurance Education Hub</h1>
                <p>Learn about insurance in simple language. Listen to audio guides.</p>
            </div>

            <div className="education-grid">
                {topics.map(topic => (
                    <div key={topic.id} className="edu-card" style={{ height: 'auto' }}>
                        <div className="edu-icon" style={{ color: topic.color, background: `${topic.color}20` }}>
                            {topic.icon}
                        </div>
                        <h3>{topic.title}</h3>
                        <p>{topic.desc}</p>

                        <div className="edu-actions">
                            <button
                                className={`edu-btn ${playingTopic === topic.title ? 'active-audio' : ''}`}
                                onClick={() => handleListen(topic)}
                                disabled={loading && playingTopic === topic.title}
                            >
                                {loading && playingTopic === topic.title ? (
                                    <span>Loading...</span>
                                ) : playingTopic === topic.title ? (
                                    <><PlayCircle size={18} fill="currentColor" /> Stop</>
                                ) : (
                                    <><PlayCircle size={18} /> Listen Guide</>
                                )}
                            </button>
                            <button
                                className={`edu-btn outline ${expandedTopic === topic.title ? 'active' : ''}`}
                                onClick={() => setExpandedTopic(expandedTopic === topic.title ? null : topic.title)}
                            >
                                <BookOpen size={18} /> {expandedTopic === topic.title ? 'Close' : 'Read More'}
                            </button>
                        </div>

                        {expandedTopic === topic.title && (
                            <div className="expanded-content" style={{ marginTop: '1rem', padding: '1rem', background: 'var(--card-bg)', borderRadius: '8px', border: '1px solid var(--border-color)', textAlign: 'left' }}>
                                <h4 style={{ marginBottom: '0.5rem', color: topic.color }}>Detailed Guide: {topic.title}</h4>
                                <p style={{ fontSize: '0.95rem', lineHeight: '1.6', color: 'var(--text-secondary)' }}>
                                    {content[topic.title]?.[`detailed_${currentLang}`] || content[topic.title]?.['detailed_en'] || "Detailed guide coming soon..."}
                                </p>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default EducationPage;
