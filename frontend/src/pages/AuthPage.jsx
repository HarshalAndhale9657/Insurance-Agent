import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, ArrowRight, Phone, Lock, User } from 'lucide-react';

const AuthPage = () => {
    const [isLogin, setIsLogin] = useState(true);
    const [step, setStep] = useState('phone'); // 'phone' or 'otp'
    const [phone, setPhone] = useState('');
    const [otp, setOtp] = useState('');
    const navigate = useNavigate();

    const handleSendOtp = (e) => {
        e.preventDefault();
        if (phone.length === 10) {
            setStep('otp');
        } else {
            alert("Please enter a valid 10-digit number");
        }
    };

    const handleVerifyOtp = (e) => {
        e.preventDefault();
        if (otp === '1234') { // Mock OTP
            navigate('/dashboard');
        } else {
            alert("Invalid OTP (Try 1234)");
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <ShieldCheck size={48} className="auth-logo" />
                    <h2>{isLogin ? 'Welcome Back' : 'Create Account'}</h2>
                    <p>{isLogin ? 'Login to manage your insurance' : 'Sign up for smart protection'}</p>
                </div>

                {step === 'phone' ? (
                    <form onSubmit={handleSendOtp} className="auth-form">
                        {!isLogin && (
                            <div className="input-group">
                                <User size={20} className="input-icon" />
                                <input type="text" placeholder="Full Name" required />
                            </div>
                        )}

                        <div className="input-group">
                            <Phone size={20} className="input-icon" />
                            <input
                                type="tel"
                                placeholder="Mobile Number"
                                value={phone}
                                onChange={(e) => setPhone(e.target.value)}
                                maxLength="10"
                                required
                            />
                        </div>

                        <button type="submit" className="primary-btn">
                            Get OTP <ArrowRight size={20} />
                        </button>
                    </form>
                ) : (
                    <form onSubmit={handleVerifyOtp} className="auth-form">
                        <div className="otp-info">
                            Enter OTP sent to +91 {phone} <br />
                            <span className="otp-hint">(Use 1234)</span>
                        </div>

                        <div className="input-group">
                            <Lock size={20} className="input-icon" />
                            <input
                                type="text"
                                placeholder="Enter 4-digit OTP"
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                maxLength="4"
                                required
                            />
                        </div>

                        <button type="submit" className="primary-btn">
                            Verify & Login <ArrowRight size={20} />
                        </button>
                        <button type="button" className="text-btn" onClick={() => setStep('phone')}>
                            Change Number
                        </button>
                    </form>
                )}

                <div className="auth-footer">
                    <p>
                        {isLogin ? "Don't have an account? " : "Already have an account? "}
                        <span onClick={() => { setIsLogin(!isLogin); setStep('phone'); }} className="link-text">
                            {isLogin ? 'Sign Up' : 'Login'}
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AuthPage;
