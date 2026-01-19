import React, { useState, useRef } from 'react';
import { Send, Mic, Square } from 'lucide-react';

const InputArea = ({ onSendMessage, isLoading }) => {
    const [text, setText] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if ((!text.trim() && !isRecording) || isLoading) return;

        onSendMessage(text);
        setText('');
    };

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;
            audioChunksRef.current = [];

            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunksRef.current.push(event.data);
                }
            };

            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
                const audioFile = new File([audioBlob], "voice_note.wav", { type: 'audio/wav' });
                onSendMessage(null, audioFile);

                // Stop all tracks
                stream.getTracks().forEach(track => track.stop());
            };

            mediaRecorder.start();
            setIsRecording(true);
        } catch (err) {
            console.error("Error accessing microphone:", err);
            alert("Could not access microphone.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && isRecording) {
            mediaRecorderRef.current.stop();
            setIsRecording(false);
        }
    };

    return (
        <div className="input-area">
            <div className="input-container">
                <input
                    type="text"
                    className="chat-input"
                    placeholder={isRecording ? "Recording..." : "Type your message..."}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    disabled={isLoading || isRecording}
                    onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)}
                />

                {!text && (
                    <button
                        className={`action-btn ${isRecording ? 'pulse' : ''}`}
                        onClick={isRecording ? stopRecording : startRecording}
                        type="button"
                        style={{ color: isRecording ? '#ef4444' : undefined }}
                    >
                        {isRecording ? <Square size={20} /> : <Mic size={20} />}
                    </button>
                )}
            </div>

            <button
                className="send-btn"
                onClick={handleSubmit}
                disabled={(!text && !isRecording) || isLoading}
            >
                <Send size={20} />
            </button>
        </div>
    );
};

export default InputArea;
