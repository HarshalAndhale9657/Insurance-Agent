import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, AlertCircle, CheckCircle, ArrowRight, FileText } from 'lucide-react';

const DashboardPage = () => {

    // Mock Data
    const recommendations = [
        {
            id: 1,
            title: 'Family Health Guard',
            provider: 'HDFC Ergo',
            cover: '₹ 10 Lakhs',
            premium: '₹ 12,500 / yr',
            tags: ['Health', 'Family']
        },
        {
            id: 2,
            title: 'iTerm Prime',
            provider: 'Max Life',
            cover: '₹ 1 Crore',
            premium: '₹ 9,000 / yr',
            tags: ['Life', 'Term']
        }
    ];

    const savedPolicies = [
        {
            id: 101,
            name: 'Bajaj Allianz Drive Protect',
            type: 'Vehicle',
            expiry: '12 Aug 2026',
            status: 'Active',
            docUrl: '#'
        },
        {
            id: 102,
            name: 'Star Health Comprehensive',
            type: 'Health',
            expiry: 'Expires in 15 days',
            status: 'Expiring Soon',
            docUrl: '#'
        }
    ];

    return (
        <div className="page-container">
            <div className="dashboard-header">
                <h1>Hello, User! 👋</h1>
                <p>Here are your personalized insurance insights.</p>
            </div>

            {/* Application Progress Tracker */}
            <div className="progress-section dash-card mb-4">
                <h3>Application Status: <span style={{ color: 'var(--primary)' }}>Verification Pending</span></h3>
                <div className="progress-stepper">
                    <div className="p-step completed">
                        <div className="p-circle">✓</div>
                        <span>Applied</span>
                    </div>
                    <div className="p-line completed"></div>
                    <div className="p-step active">
                        <div className="p-circle">2</div>
                        <span>Docs Review</span>
                    </div>
                    <div className="p-line"></div>
                    <div className="p-step">
                        <div className="p-circle">3</div>
                        <span>Issued</span>
                    </div>
                </div>
            </div>

            <div className="dashboard-grid">
                {/* Risk Assessment Card */}
                <div className="dash-card risk-card">
                    <div className="card-header">
                        <AlertCircle size={24} />
                        <h3>Risk Coverage Score</h3>
                    </div>
                    <div className="score-circle">
                        <span className="sc-val">65</span>
                        <span className="sc-max">/100</span>
                    </div>
                    <p>You are missing <strong>Critical Illness</strong> cover. Chat with our assistant to upgrade.</p>
                    <Link to="/chat" className="dash-btn primary">Improve Score</Link>
                </div>

                {/* Saved Policies */}
                <div className="dash-card">
                    <div className="card-header">
                        <Shield size={24} color="#059669" />
                        <h3>Your Policies</h3>
                    </div>
                    <div className="policies-list">
                        {savedPolicies.map(policy => (
                            <div key={policy.id} className="policy-item">
                                <div>
                                    <div className="policy-name">{policy.name}</div>
                                    <div className={`policy-status ${policy.status === 'Expiring Soon' ? 'warn' : 'ok'}`}>
                                        {policy.expiry}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                    <Link to="/documents" className="dash-btn">View All Documents</Link>
                </div>
            </div>

            <h2 style={{ marginTop: '3rem', marginBottom: '1.5rem', color: 'var(--text-primary)' }}>Recommended Plans</h2>

            <div className="recommendations-grid">
                {recommendations.map(plan => (
                    <div key={plan.id} className="plan-card">
                        <div className="plan-badge">{plan.provider}</div>
                        <h3>{plan.title}</h3>
                        <div className="plan-details">
                            <div className="detail-item">
                                <span>Cover</span>
                                <strong>{plan.cover}</strong>
                            </div>
                            <div className="detail-item">
                                <span>Est. Cost</span>
                                <strong>{plan.premium}</strong>
                            </div>
                        </div>
                        <div className="tags">
                            {plan.tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
                        </div>
                        <div className="plan-actions">
                            <Link to="/compare" className="plan-btn outline">Compare</Link>
                            <Link to="/purchase" className="plan-btn">Get Assistance <ArrowRight size={16} /></Link>
                        </div>
                    </div>
                ))}

                <div className="plan-card start-new">
                    <FileText size={48} color="var(--primary)" />
                    <h3>Need more options?</h3>
                    <p>Answer a few questions to get tailored suggestions.</p>
                    <Link to="/chat" className="plan-btn">Start Survey</Link>
                </div>
            </div>
        </div>
    );
};

export default DashboardPage;
