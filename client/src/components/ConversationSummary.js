import React from 'react';

function ConversationSummary({ summary, onClose }) {
    if (!summary) return null;

    return (
        <div className="summary-panel">
            <div className="summary-header">
                <h3>Conversation Summary</h3>
                <button className="close-btn" onClick={onClose}>X</button>
            </div>
            <div className="summary-content">{summary.content}</div>
        </div>
    );
}

export default ConversationSummary;
