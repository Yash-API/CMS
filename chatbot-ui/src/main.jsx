import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles/index.css' // ✅ Updated path after moving index.css to styles folder

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
