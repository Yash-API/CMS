import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./Login";
import Chatbot from "./Chatbot";
import ProtectedRoute from "./ProtectedRoute";
import AddUser from "./AddUser";

export default function App() {
  return (
    <Router>
      <Routes>
        {/* Public Route */}
        <Route path="/login" element={<Login />} />

        {/* Protected Routes */}
        <Route
          path="/add/:type"
          element={
            <ProtectedRoute>
              <AddUser />
            </ProtectedRoute>
          }
        />
        <Route
          path="/chatbot"
          element={
            <ProtectedRoute>
              <Chatbot />
            </ProtectedRoute>
          }
        />

        {/* Redirect all other routes to login */}
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}
