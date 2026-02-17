import React, { useState } from 'react';
import { User, Mail, Phone, MapPin, Calendar, Briefcase, Save, Edit2 } from 'lucide-react';

const ProfilePage = () => {
    const [isEditing, setIsEditing] = useState(false);
    const [user, setUser] = useState({
        name: 'Harshal Andhale',
        email: 'harshal@example.com',
        phone: '+91 98765 43210',
        dob: '1995-08-15',
        gender: 'Male',
        address: '123, Green Park, Pune, Maharashtra',
        occupation: 'Software Engineer'
    });

    const handleChange = (e) => {
        setUser({ ...user, [e.target.name]: e.target.value });
    };

    const handleSave = () => {
        setIsEditing(false);
        // Here you would typically save to backend
        console.log('Saved user:', user);
    };

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>User Profile</h1>
                <p>Manage your personal information and account details.</p>
            </div>

            <div className="profile-container">
                <div className="profile-card">
                    <div className="profile-header">
                        <div className="avatar-large">
                            {user.name.charAt(0)}
                        </div>
                        <div className="profile-title">
                            <h2>{user.name}</h2>
                            <p>{user.occupation}</p>
                        </div>
                        <button 
                            className={`edit-btn ${isEditing ? 'active' : ''}`}
                            onClick={() => isEditing ? handleSave() : setIsEditing(true)}
                        >
                            {isEditing ? <><Save size={18} /> Save</> : <><Edit2 size={18} /> Edit</>}
                        </button>
                    </div>

                    <div className="profile-details-grid">
                        <div className="input-group">
                            <label><User size={16} /> Full Name</label>
                            <input 
                                type="text" 
                                name="name" 
                                value={user.name} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                            />
                        </div>

                        <div className="input-group">
                            <label><Mail size={16} /> Email Address</label>
                            <input 
                                type="email" 
                                name="email" 
                                value={user.email} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                            />
                        </div>

                        <div className="input-group">
                            <label><Phone size={16} /> Phone Number</label>
                            <input 
                                type="tel" 
                                name="phone" 
                                value={user.phone} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                            />
                        </div>

                        <div className="input-group">
                            <label><Calendar size={16} /> Date of Birth</label>
                            <input 
                                type="date" 
                                name="dob" 
                                value={user.dob} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                            />
                        </div>

                        <div className="input-group">
                            <label><User size={16} /> Gender</label>
                            <select 
                                name="gender" 
                                value={user.gender} 
                                onChange={handleChange} 
                                disabled={!isEditing}
                            >
                                <option>Male</option>
                                <option>Female</option>
                                <option>Other</option>
                            </select>
                        </div>

                        <div className="input-group">
                            <label><Briefcase size={16} /> Occupation</label>
                            <input 
                                type="text" 
                                name="occupation" 
                                value={user.occupation} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                            />
                        </div>

                        <div className="input-group full-width">
                            <label><MapPin size={16} /> Address</label>
                            <textarea 
                                name="address" 
                                value={user.address} 
                                onChange={handleChange} 
                                disabled={!isEditing} 
                                rows="3"
                            />
                        </div>
                    </div>
                </div>
            </div>
            
            <style>{`
                .profile-container {
                    max-width: 800px;
                    margin: 0 auto;
                }
                .profile-card {
                    background: white;
                    border-radius: 16px;
                    padding: 2rem;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                }
                .profile-header {
                    display: flex;
                    align-items: center;
                    gap: 1.5rem;
                    border-bottom: 1px solid #e2e8f0;
                    padding-bottom: 2rem;
                    margin-bottom: 2rem;
                }
                .avatar-large {
                    width: 80px;
                    height: 80px;
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
                    color: white;
                    font-size: 2.5rem;
                    font-weight: bold;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                .profile-title h2 {
                    margin: 0;
                    font-size: 1.5rem;
                    color: #1e293b;
                }
                .profile-title p {
                    margin: 0.25rem 0 0;
                    color: #64748b;
                }
                .edit-btn {
                    margin-left: auto;
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    border: 1px solid #e2e8f0;
                    background: white;
                    color: #475569;
                    cursor: pointer;
                    transition: all 0.2s;
                }
                .edit-btn:hover {
                    background: #f8fafc;
                    border-color: #cbd5e1;
                }
                .edit-btn.active {
                    background: #3b82f6;
                    color: white;
                    border-color: #3b82f6;
                }
                .profile-details-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 1.5rem;
                }
                .input-group {
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                }
                .input-group.full-width {
                    grid-column: 1 / -1;
                }
                .input-group label {
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                    font-size: 0.875rem;
                    color: #64748b;
                    font-weight: 500;
                }
                .input-group input, .input-group select, .input-group textarea {
                    padding: 0.75rem;
                    border: 1px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 1rem;
                    color: #1e293b;
                    background: #f8fafc;
                    transition: all 0.2s;
                }
                .input-group input:disabled, .input-group select:disabled, .input-group textarea:disabled {
                    background: transparent;
                    border-color: transparent;
                    padding-left: 0;
                    color: #334155;
                    font-weight: 500;
                    cursor: default;
                }
                .input-group input:focus, .input-group select:focus, .input-group textarea:focus {
                    outline: none;
                    border-color: #3b82f6;
                    background: white;
                    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                }
            `}</style>
        </div>
    );
};

export default ProfilePage;
