import React from 'react';

function RoleSelector({ role, onChange }) {
    return (
        <div className="control-group">
            <label>Role:</label>
            <select value={role} onChange={(e) => onChange(e.target.value)}>
                <option value="doctor">Doctor</option>
                <option value="patient">Patient</option>
            </select>
        </div>
    );
}

export default RoleSelector;
