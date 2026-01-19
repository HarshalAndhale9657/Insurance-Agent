import React from 'react';
import { Check, X, ArrowLeft } from 'lucide-react';
import { Link } from 'react-router-dom';

const ComparePage = () => {
    return (
        <div className="page-container">
            <div className="page-header">
                <Link to="/dashboard" style={{ position: 'absolute', left: '2rem', display: 'flex', alignItems: 'center', gap: '0.5rem', textDecoration: 'none', color: 'var(--text-secondary)' }}>
                    <ArrowLeft size={20} /> Back
                </Link>
                <h1>Plan Comparison</h1>
                <p>Comparing 2 Selected Plans</p>
            </div>

            <div className="comparison-table-wrapper">
                <table className="comparison-table">
                    <thead>
                        <tr>
                            <th>Features</th>
                            <th>Family Health Guard</th>
                            <th>iTerm Prime</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Provider</td>
                            <td><strong>HDFC Ergo</strong></td>
                            <td><strong>Max Life</strong></td>
                        </tr>
                        <tr>
                            <td>Cover Amount</td>
                            <td>₹ 10 Lakhs</td>
                            <td>₹ 1 Crore</td>
                        </tr>
                        <tr>
                            <td>Est. Contribution</td>
                            <td>₹ 12,500 / yr</td>
                            <td>₹ 9,000 / yr</td>
                        </tr>
                        <tr>
                            <td>Cashless Hospitals</td>
                            <td>12,000+</td>
                            <td>N/A</td>
                        </tr>
                        <tr>
                            <td>Claim Settlement</td>
                            <td>98.5%</td>
                            <td>99.3%</td>
                        </tr>
                        <tr>
                            <td>Medical Checkup</td>
                            <td><Check size={20} color="green" /> Not Required</td>
                            <td><Check size={20} color="green" /> Video Medical</td>
                        </tr>
                        <tr>
                            <td></td>
                            <td>
                                <Link to="/purchase" className="plan-btn">Get Support</Link>
                            </td>
                            <td>
                                <Link to="/purchase" className="plan-btn outline">Get Support</Link>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ComparePage;
