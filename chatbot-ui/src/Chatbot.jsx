import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function Chatbot() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  const handleSend = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse("");

    try {
      const res = await axios.post(
        "http://localhost:8000/api/chatbot/convert-to-sql",
        { text: question },
        {
      headers: {
        Authorization: `Bearer ${token}`,
      },
        }
      );

      setResponse(res.data.response || "✅ Success but no response returned.");
    } catch (err) {
      console.error(err);
      setResponse("❌ " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/login");
  };

  return (
    <div className="chatbot-container">
      <div className="chatbot-header">
        <h1 className="chatbot-title">🤖 Chat with your SQL Assistant</h1>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="chatbot-input-group">
        <input
          type="text"
          className="chatbot-input"
          placeholder="Ask something like 'Show client names'"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          disabled={loading}
          className="chatbot-send-button"
        >
          {loading ? "Loading..." : "Send"}
        </button>
      </div>

      <div className="chatbot-response">
        <p>{response || "Response will appear here."}</p>
      </div>
    </div>
  );
}
