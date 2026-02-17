import React from 'react';
import ReactMarkdown from 'react-markdown';
import { User, Bot, Play, FileText } from 'lucide-react';

const Message = ({ message }) => {
    const isBot = message.sender === 'bot';

    return (
        <div className={`message-wrapper ${isBot ? 'bot' : 'user'}`}>
            <div className="avatar">
                {isBot ? <Bot size={18} /> : <User size={18} />}
            </div>

            <div className="message-content">
                {/* Text / Markdown */}
                <div className="markdown">
                    <ReactMarkdown>{message.text}</ReactMarkdown>
                </div>

                {/* Audio Player */}
                {message.audioUrl && (isBot || message.sender === 'bot') && (
                    <div className="audio-player">
                        <audio controls preload="metadata" src={message.audioUrl} style={{ width: '100%', height: '30px' }} />
                    </div>
                )}

                {/* PDF / Media Attachment */}
                {message.mediaUrl && message.mediaType === 'application/pdf' && (
                    <div className="media-attachment" style={{ marginTop: '10px' }}>
                        <a href={message.mediaUrl} target="_blank" rel="noopener noreferrer" style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#2563eb', textDecoration: 'none', background: 'white', padding: '8px', borderRadius: '8px' }}>
                            <FileText size={20} />
                            <span>View Attachment (PDF)</span>
                        </a>
                    </div>
                )}

                {/* Timestamp */}
                <div className="timestamp">
                    {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
            </div>
        </div>
    );
};

export default Message;
