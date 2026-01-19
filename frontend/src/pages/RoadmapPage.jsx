import React from 'react';
import { Flag, Download, Calendar, ArrowRight } from 'lucide-react';

const RoadmapPage = () => {

    const milestones = [
        { year: '2024', title: 'Start Phase', desc: 'Secure Health & Life basics.', status: 'completed' },
        { year: '2026', title: 'Asset Protection', desc: 'Add Vehicle & Home insurance.', status: 'current' },
        { year: '2029', title: 'Wealth Review', desc: 'Increase Life cover for family growth.', status: 'future' },
        { year: '2035', title: 'Retirement Prep', desc: 'Start Pension & Annuity plans.', status: 'future' }
    ];

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Insurance Roadmap</h1>
                <p>Your step-by-step journey to full financial security.</p>
            </div>

            <div className="roadmap-timeline">
                <div className="timeline-line"></div>
                {milestones.map((m, index) => (
                    <div key={index} className={`timeline-item ${m.status}`}>
                        <div className="t-marker">
                            {m.status === 'completed' && '✓'}
                            {m.status === 'current' && <div className="current-dot"></div>}
                        </div>
                        <div className="t-content">
                            <span className="t-year">{m.year}</span>
                            <h3>{m.title}</h3>
                            <p>{m.desc}</p>
                        </div>
                    </div>
                ))}
            </div>

            <div className="download-section">
                <button className="primary-btn download-btn">
                    <Download size={20} /> Download My Roadmap (PDF)
                </button>
            </div>
        </div>
    );
};

export default RoadmapPage;
