import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Login.css";


// Use API URL from env or fallback to localhost
const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    console.log("✅ VITE_API_URL:", API_URL);
  }, []);

  const login = async () => {
    try {
      debugger; // Breakpoint
      const params = new URLSearchParams();
      params.append("username", email);
      params.append("password", password);

      console.log("🔐 Sending login request to:", `${API_URL}/api/auth/login`);

      const res = await axios.post(`${API_URL}/api/auth/login`, params, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const token = res.data.access_token;
      console.log("✅ Login Success. Token:", token);

      localStorage.setItem("access_token", token);
      navigate("/chatbot");
    } catch (err) {
      console.error("❌ Login failed:", err);
      setError("Login failed. Please try again.");
    }
  };

  return (
    <div className="login-container">
      <h2 className="login-title">Welcome Back</h2>
      <input
        type="text"
        className="login-input"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        className="login-input"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {error && <p className="login-error">{error}</p>}
      <button className="login-button" onClick={login}>
        Login
      </button>
    </div>
  );
}
