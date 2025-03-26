import { useState } from "react";
import axios from "axios";

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    try {
      // Replace with your backend chatbot API if needed
      const response = await axios.post("URL of our api", {
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: input }],
      }, {
        headers: {
          "Authorization": `Bearer YOUR_OPENAI_API_KEY`,
          "Content-Type": "application/json",
        },
      });

      setMessages([...newMessages, { text: response.data.choices[0].message.content, sender: "bot" }]);
    } catch (error) {
      console.error("Chatbot error:", error);
    }
  };

  return (
    <div style={{ position: "fixed", bottom: 20, right: 20, width: "300px", border: "1px solid #ccc", borderRadius: "10px", padding: "10px", backgroundColor: "#fff" }}>
      <div style={{ height: "200px", overflowY: "auto", marginBottom: "10px" }}>
        {messages.map((msg, index) => (
          <div key={index} style={{ textAlign: msg.sender === "user" ? "right" : "left", marginBottom: "5px" }}>
            <span style={{ display: "inline-block", padding: "5px 10px", borderRadius: "10px", backgroundColor: msg.sender === "user" ? "#007bff" : "#ddd", color: msg.sender === "user" ? "#fff" : "#000" }}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <input type="text" value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type a message..." style={{ width: "80%" }} />
      <button onClick={sendMessage} style={{ width: "18%", marginLeft: "2%" }}>Send</button>
    </div>
  );
};

export default Chatbot;
