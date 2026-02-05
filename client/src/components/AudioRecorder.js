import React from 'react';

function AudioRecorder({ isRecording, onStart, onStop }) {
    return (
        <div className="audio-controls">
            {isRecording ? (
                <button className="record-btn recording" onClick={onStop}>
                    <span>Recording... (Click to Stop)</span>
                </button>
            ) : (
                <button className="record-btn" onClick={onStart}>
                    <span>🎤 Record Audio</span>
                </button>
            )}
        </div>
    );
}

export default AudioRecorder;
