import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState } from 'react'
import BirthDetailsForm from './components/BirthDetailsForm'
import ChartsPage from './components/ChartsPage'
import PredictionsPage from './components/PredictionsPage'
import './App.css'

function App() {
  const [chartData, setChartData] = useState(null)

  return (
    <Router>
      <div className="app">
        <header className="app-header">
          <h1>🌟 Gopi Astro</h1>
          <p>AI-Powered Vedic Predictions</p>
        </header>

        <Routes>
          <Route path="/" element={<BirthDetailsForm setChartData={setChartData} />} />
          <Route path="/charts" element={chartData ? <ChartsPage chartData={chartData} /> : <Navigate to="/" />} />
          <Route path="/predictions" element={chartData ? <PredictionsPage chartData={chartData} /> : <Navigate to="/" />} />
        </Routes>

        <footer className="app-footer">
          <p>AI-Powered Vedic Predictions</p>
          <p><a href="http://127.0.0.1:8000/docs" target="_blank" rel="noopener noreferrer">API Documentation</a></p>
        </footer>
      </div>
    </Router>
  )
}

export default App
