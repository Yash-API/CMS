import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<h1 className="text-center mt-5">Dashboard</h1>} />
      </Routes>
    </Router>
  );
}

export default App;
