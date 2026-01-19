import React, { useState } from 'react';
import { CheckCircle, Upload, CreditCard } from 'lucide-react';

const PurchasePage = () => {
    const [step, setStep] = useState(1);

    return (
        <div className="page-container">
            <div className="page-header">
                <h1>Application Assistance</h1>
                <p>Helping you apply for: Family Health Guard</p>
            </div>

            <div className="purchase-stepper">
                <div className={`step ${step >= 1 ? 'active' : ''}`}>1. Details</div>
                <div className={`step-line ${step >= 2 ? 'active' : ''}`}></div>
                <div className={`step ${step >= 2 ? 'active' : ''}`}>2. Documents</div>
                <div className={`step-line ${step >= 3 ? 'active' : ''}`}></div>
                <div className={`step ${step >= 3 ? 'active' : ''}`}>3. Submit</div>
            </div>

            <div className="purchase-content">
                {step === 1 && (
                    <div className="step-content">
                        <h3>Applicant Details</h3>
                        <div className="form-grid">
                            <input type="text" placeholder="Full Name (as per Aadhaar)" className="form-input" />
                            <input type="text" placeholder="Date of Birth" className="form-input" />
                            <input type="text" placeholder="PAN Number" className="form-input" />
                            <input type="text" placeholder="Nominee Name" className="form-input" />
                        </div>
                        <button className="primary-btn" onClick={() => setStep(2)}>Next: Verify Docs</button>
                    </div>
                )}

                {step === 2 && (
                    <div className="step-content">
                        <h3>Document Verification Support</h3>
                        <div className="doc-upload-box">
                            <div className="doc-item">
                                <span>Aadhar Card</span>
                                <button className="upload-btn"><Upload size={16} /> Select File</button>
                            </div>
                            <div className="doc-item">
                                <span>PAN Card</span>
                                <div className="uploaded"><CheckCircle size={16} /> Verified</div>
                            </div>
                            <div className="doc-item">
                                <span>Passport Photo</span>
                                <button className="upload-btn"><Upload size={16} /> Select File</button>
                            </div>
                        </div>
                        <button className="primary-btn" onClick={() => setStep(3)}>Next: Review</button>
                    </div>
                )}

                {step === 3 && (
                    <div className="step-content text-center">
                        <h3>Application Review</h3>
                        <p>We are verifying your details against the scheme requirements...</p>
                        <div className="payment-mock">
                            <CheckCircle size={48} color="#10b981" />
                        </div>
                        <button className="primary-btn" onClick={() => alert("Application Submitted for Processing!")}>Submit Application</button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PurchasePage;
