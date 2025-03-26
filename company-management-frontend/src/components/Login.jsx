import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [contactOrEmail, setContactOrEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      // Convert data to URL-encoded format
      const formData = new URLSearchParams();
      formData.append("username", contactOrEmail); // FastAPI expects "username"
      formData.append("password", password);

      const response = await axios.post("http://127.0.0.1:8000/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });

      if (response.data.access_token) {
        localStorage.setItem("token", response.data.access_token);
        navigate("/dashboard");
      }
    } catch (err) {
      setError("Invalid contact/email or password. Please try again.");
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100 bg-light">
      <div className="card shadow p-4" style={{ width: "350px" }}>
        <h2 className="text-center text-primary mb-3">Login</h2>
        {error && <p className="text-danger text-center">{error}</p>}
        <form onSubmit={handleLogin}>
          <div className="mb-3">
            <label className="form-label">Contact or Email</label>
            <input
              type="text"
              className="form-control"
              placeholder="Enter your contact or email"
              value={contactOrEmail}
              onChange={(e) => setContactOrEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-control"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Login
          </button>
        </form>
      </div>
    </div>
  );
};

export default Login;
