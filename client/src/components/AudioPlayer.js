import React from 'react';

function AudioPlayer({ src }) {
    if (!src) return null;

    return (
        <div className="message-audio">
            <audio controls src={src} />
        </div>
    );
}

export default AudioPlayer;
