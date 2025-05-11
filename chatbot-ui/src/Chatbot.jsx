import { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import "./styles/Chatbot.css";


const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const fieldMap = {
  employee: ["name", "role", "salary", "joining_date", "dob"],
  client: [
    "name",
    "budget",
    "project_description",
    "project_start_date",
    "project_end_date",
  ],
};

export default function Chatbot() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [loading, setLoading] = useState(false);
  const [suggestedFields, setSuggestedFields] = useState(null);
  const token = localStorage.getItem("access_token");
  const navigate = useNavigate();

  useEffect(() => {
    const lower = question.toLowerCase();
    if (lower.includes("add employee")) {
      setSuggestedFields(fieldMap.employee);
    } else if (lower.includes("add client")) {
      setSuggestedFields(fieldMap.client);
    } else {
      setSuggestedFields(null);
    }
  }, [question]);

  const handleSend = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setResponse("");
    setSuggestedFields(null); // Hide field tip after submit

    try {
      const res = await axios.post(
        `${API_URL}/api/chatbot/convert-to-sql`,
        { text: question },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const result = res.data;
      console.log("✅ Response:", result);

      const lowerQuestion = result.question?.toLowerCase() || "";

      if (
        result.response?.toLowerCase().includes("insert executed successfully")
      ) {
        // Format smart message for employee/client
        const parts = result.question
          .replace(/add (employee|client)/i, "")
          .split(",")
          .map((p) => p.trim());

        const label = lowerQuestion.includes("employee") ? "employee" : "client";
        const fields = fieldMap[label];

        const formatted = fields
          .map((key, i) => `**${key}**: ${parts[i] || "(missing)"}`)
          .join(", ");

        setResponse(`✅ Successfully added ${label} — ${formatted}`);
      } else {
        setResponse(result.response || "✅ Success but no response returned.");
      }
    } catch (err) {
      console.error("❌ Axios Error:", err);
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
          placeholder="Ask something like 'Add employee'"
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

      {suggestedFields && (
        <div
          style={{
            background: "#fef9c3",
            border: "1px solid #fde047",
            borderRadius: "8px",
            padding: "12px 16px",
            marginBottom: "16px",
            textAlign: "left",
            fontSize: "0.95rem",
            color: "#92400e",
          }}
        >
          <strong>Tip:</strong> To add a {question.toLowerCase().includes("employee") ? "employee" : "client"}, provide:
          <ul style={{ marginTop: "6px", paddingLeft: "20px" }}>
            {suggestedFields.map((field) => (
              <li key={field}>{field}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="chatbot-response">
        <p>{response || "Response will appear here."}</p>
      </div>
    </div>
  );
}
