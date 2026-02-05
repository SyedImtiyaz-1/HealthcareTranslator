import React from 'react';
import { getAudioUrl } from '../services/api';

function MessageBubble({ message }) {
    const formatTime = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    };

    return (
        <div className={`message ${message.role}`}>
            <div className="message-header">{message.role}</div>
            <div className="message-bubble">
                <div className="message-original">{message.original_text}</div>
                {message.translated_text && message.translated_text !== message.original_text && (
                    <div className="message-translated">{message.translated_text}</div>
                )}
                {message.audio_path && (
                    <div className="message-audio">
                        <audio controls src={getAudioUrl(message.audio_path)} />
                    </div>
                )}
            </div>
            <div className="message-time">{formatTime(message.created_at)}</div>
        </div>
    );
}

export default MessageBubble;
