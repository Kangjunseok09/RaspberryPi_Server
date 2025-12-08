import './App.css'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home.jsx'
import WaterLevel from './pages/WaterLevel.jsx'
import WaterLevelNotification from './pages/WaterLevelNotification.jsx'
import Setting from './pages/Setting.jsx'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/water-level" element={<WaterLevel />} />
        <Route path="/water-level-notification" element={<WaterLevelNotification />} />
        <Route path="/setting" element={<Setting />} />
      </Routes>
    </Router>
  )
}

export default App
