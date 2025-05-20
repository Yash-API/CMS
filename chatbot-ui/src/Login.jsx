import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Login.css";

// API URLs from environment variables
const API_URL_LOCAL = import.meta.env.VITE_API_URL_LOCAL;
const API_URL_LAN = import.meta.env.VITE_API_URL_LAN;

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    console.log("✅ API_URL_LOCAL:", API_URL_LOCAL);
    console.log("✅ API_URL_LAN:", API_URL_LAN);
  }, []);

  const login = async () => {
    const endpoints = [API_URL_LOCAL, API_URL_LAN];

    for (let baseUrl of endpoints) {
      try {
        const params = new URLSearchParams();
        params.append("username", email);
        params.append("password", password);

        const apiUrl = `${baseUrl}/api/auth/login`;
        console.log("🔐 Trying login at:", apiUrl);

        const res = await axios.post(apiUrl, params, {
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          withCredentials: false,
          timeout: 8000,
          validateStatus: (status) => status >= 200 && status < 500,
        });

        if (res.status === 200) {
          const token = res.data.access_token;
          console.log("✅ Login Success. Token:", token);
          localStorage.setItem("access_token", token);
          localStorage.setItem("api_base_url", baseUrl); // Save the working base URL
          navigate("/chatbot");
          return; // Exit after success
        } else {
          console.warn(`❌ Login failed with status ${res.status} from ${baseUrl}`);
        }
      } catch (err) {
        console.warn(`⚠️ Error with ${baseUrl}:`, err.message);
      }
    }

    // Final fallback message if none succeed
    setError("Login failed. Server unreachable or invalid credentials.");
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
