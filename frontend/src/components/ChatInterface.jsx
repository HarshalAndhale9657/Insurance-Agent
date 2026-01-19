import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import Message from './Message';
import InputArea from './InputArea';
import { Loader2 } from 'lucide-react';

const API_URL = 'http://localhost:8000/api';

const ChatInterface = ({ language }) => {
    const [messages, setMessages] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState('');
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Generate or retrieve session ID
        let storedSession = localStorage.getItem('chat_session_id');
        if (!storedSession) {
            storedSession = 'web_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('chat_session_id', storedSession);
        }
        setSessionId(storedSession);

        // Initial greeting based on language
        const greetings = {
            en: "🙏 **Namaste! I am 'Suraksha Sahayak'.**\n\nI can help you find the perfect insurance plan. To get started, may I know your **full name**?",
            hi: "🙏 **नमस्ते! मैं 'सुरक्षा सहायक' हूँ।**\n\nमैं आपको सही बीमा योजना खोजने में मदद कर सकता हूँ। शुरू करने के लिए, क्या मैं आपका **पूरा नाम** जान सकता हूँ?",
            mr: "🙏 **नमस्कार! मी 'सुरक्षा सहाय्यक' आहे.**\n\nमी तुम्हाला योग्य विमा योजना शोधण्यात मदत करू शकतो. सुरू करण्यासाठी, कृपया मला तुमचे **पूर्ण नाव** सांगाल का?"
        };

        setMessages([
            {
                id: 'init-1',
                sender: 'bot',
                text: greetings[language] || greetings.en,
                timestamp: new Date().toISOString()
            }
        ]);
    }, [language]); // Re-run if language changes (optional, but good for testing)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSendMessage = async (text, file = null) => {
        // Add User Message
        const newUserMsg = {
            id: Date.now().toString(),
            sender: 'user',
            text: text || (file ? "🎤 Voice Message" : ""),
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, newUserMsg]);
        setIsLoading(true);

        try {
            let response;
            if (file) {
                // Audio Upload
                const formData = new FormData();
                formData.append('session_id', sessionId);
                formData.append('file', file);
                response = await axios.post(`${API_URL}/audio`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
            } else {
                // Text Message
                response = await axios.post(`${API_URL}/chat`, {
                    session_id: sessionId,
                    message: text
                });
            }

            const data = response.data;

            // Add Bot Message
            const newBotMsg = {
                id: Date.now().toString() + '_bot',
                sender: 'bot',
                text: data.response_text,
                audioUrl: data.audio_url || data.media_url, // Generic media handler
                mediaType: data.media_type,
                timestamp: new Date().toISOString()
            };

            setMessages(prev => [...prev, newBotMsg]);

            // Auto-play audio if present? 
            // Let's leave it to user to click play for now to avoid auto-play policy issues.

        } catch (error) {
            console.error("Error sending message:", error);
            const errorMsg = {
                id: Date.now().toString() + '_error',
                sender: 'bot',
                text: "⚠️ Sorry, I'm having trouble connecting to the server.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-interface">
            <div className="chat-area">
                {messages.map(msg => (
                    <Message key={msg.id} message={msg} />
                ))}
                {isLoading && (
                    <div className="message-wrapper bot">
                        <div className="avatar">🤖</div>
                        <div className="message-content">
                            <Loader2 className="animate-spin" size={20} />
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>
            <InputArea onSendMessage={handleSendMessage} isLoading={isLoading} />
        </div>
    );
};

export default ChatInterface;
