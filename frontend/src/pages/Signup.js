// src/pages/Signup.js
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api/api';

function Signup() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      await API.post('/signup', { email, password });
      alert('Signup successful! Please log in.');
      navigate('/');
    } catch (err) {
      alert('Signup failed');
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <form onSubmit={handleSignup}>
        <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit">Sign Up</button>
      </form>
      <p>Already have an account? <Link to="/">Login</Link></p>
    </div>
  );
}

export default Signup;
