import React, { useState } from "react";
import { loginUser } from "../api/authService";
import { useHistory } from "react-router-dom";
import "./auth.css";

export const Login = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const history = useHistory();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await loginUser(username, password);
      localStorage.setItem("token", res.data.access_token);
      onLoginSuccess();
      history.push("/");
    } catch (err) {
      setError("Invalid username or password");
    }
  };

  return (
    <div className="zoom-card-wide">
      <i className="fas fa-times exit-icon" onClick={() => history.push("/")} />
      <h2 className="auth-title">Login</h2>
      <form onSubmit={handleLogin} className="auth-form">
        <input
          className="auth-input"
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          className="auth-input"
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit" className="auth-button">Login</button>
        <button onClick={() => history.push("/register")} className="link-button">Don't have an account? Sign up</button>
        {error && <p className="error">{error}</p>}
      </form>
    </div>
  );
};
