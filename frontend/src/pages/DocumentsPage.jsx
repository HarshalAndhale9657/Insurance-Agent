import React, { useState } from 'react';
import { FileText, Upload, Sparkles, Check, Eye } from 'lucide-react';

const DocumentsPage = () => {

    const docs = [
        { id: 1, name: 'Aadhaar Card', status: 'Verified', date: '12 Jan 2024' },
        { id: 2, name: 'PAN Card', status: 'Pending', date: '18 Jan 2024' }
    ];

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Document Vault</h1>
                <p>Securely store and understand your insurance documents.</p>
            </div>

            <div className="doc-grid">
                {/* Upload Section */}
                <div className="doc-card upload-section">
                    <div className="upload-zone">
                        <Upload size={32} color="var(--primary)" />
                        <h3>Upload Document</h3>
                        <p>Drag & drop or click to browse</p>
                        <div className="supported-types">PDF, JPG, PNG</div>
                    </div>
                </div>

                {/* Document List */}
                <div className="doc-list-section">
                    <h3>Your Documents</h3>
                    <div className="doc-list">
                        {docs.map(doc => (
                            <div key={doc.id} className="doc-row">
                                <div className="doc-icon"><FileText size={20} /></div>
                                <div className="doc-info">
                                    <div className="doc-name">{doc.name}</div>
                                    <div className="doc-date">Uploaded on {doc.date}</div>
                                </div>
                                <div className="doc-badge" style={{
                                    background: doc.status === 'Verified' ? '#dcfce7' : '#fff7ed',
                                    color: doc.status === 'Verified' ? '#166534' : '#c2410c'
                                }}>
                                    {doc.status}
                                </div>
                                <button className="icon-btn" title="View"><Eye size={18} /></button>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* AI Explain Feature */}
            <div className="ai-explain-box">
                <div className="ai-header">
                    <Sparkles size={24} color="#7c3aed" />
                    <div className="ai-title">
                        <h3>AI Policy explainer</h3>
                        <p>Don't understand complex terms? Let AI simplify it for you.</p>
                    </div>
                </div>
                <button className="primary-btn ai-btn">
                    <Sparkles size={18} /> Analyze Latest Policy
                </button>
            </div>

        </div>
    );
};

export default DocumentsPage;
