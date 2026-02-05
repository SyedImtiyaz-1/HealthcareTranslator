import React from 'react';

function LanguageSelector({ label, language, languages, onChange }) {
    return (
        <div className="control-group">
            <label>{label}:</label>
            <select value={language} onChange={(e) => onChange(e.target.value)}>
                {languages.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                        {lang.name}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default LanguageSelector;
