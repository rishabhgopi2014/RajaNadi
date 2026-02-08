import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

function BirthDetailsForm({ setChartData }) {
    const navigate = useNavigate()
    const [formData, setFormData] = useState({
        name: '',
        date_of_birth: '',
        time_of_birth: '',
        place_of_birth: ''
    })
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [progress, setProgress] = useState(0)

    // Autocomplete state
    const [placeSuggestions, setPlaceSuggestions] = useState([])
    const [showSuggestions, setShowSuggestions] = useState(false)
    const [searchingPlaces, setSearchingPlaces] = useState(false)
    const [isPlaceSelected, setIsPlaceSelected] = useState(false)
    const suggestionsRef = useRef(null)

    // Search for places when user types
    useEffect(() => {
        const searchPlaces = async () => {
            const query = formData.place_of_birth

            // Don't search if we just selected a place
            if (isPlaceSelected || query.length < 3) {
                setPlaceSuggestions([])
                setShowSuggestions(false)
                return
            }

            setSearchingPlaces(true)

            try {
                const response = await axios.get(
                    `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=8`
                )

                // Deduplicate results based on display_name
                const uniquePlaces = []
                const seenNames = new Set()

                response.data.forEach(place => {
                    if (!seenNames.has(place.display_name)) {
                        seenNames.add(place.display_name)
                        uniquePlaces.push(place)
                    }
                })

                setPlaceSuggestions(uniquePlaces)
                // Only show if we haven't just selected (this might still be tricky)
                setShowSuggestions(uniquePlaces.length > 0)
            } catch (err) {
                console.error('Place search error:', err)
                setPlaceSuggestions([])
            } finally {
                setSearchingPlaces(false)
            }
        }

        const timeoutId = setTimeout(searchPlaces, 300)
        return () => clearTimeout(timeoutId)
    }, [formData.place_of_birth])

    // Close suggestions when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (suggestionsRef.current && !suggestionsRef.current.contains(event.target)) {
                setShowSuggestions(false)
            }
        }

        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    const handleChange = (e) => {
        if (e.target.name === 'place_of_birth') {
            setIsPlaceSelected(false)
        }
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
    }

    const handlePlaceSelect = (place) => {
        // Update state with selected place
        setFormData(prev => ({
            ...prev,
            place_of_birth: place.display_name,
            latitude: parseFloat(place.lat),
            longitude: parseFloat(place.lon)
        }))
        setIsPlaceSelected(true)
        // Clear suggestions and hide them immediately
        setPlaceSuggestions([])
        setShowSuggestions(false)
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError(null)
        setProgress(0)

        try {
            // Simulate progress during calculation
            const progressInterval = setInterval(() => {
                setProgress(prev => Math.min(prev + 10, 90))
            }, 500)

            const response = await axios.post(`${API_BASE_URL}/calculate-chart`, formData)

            clearInterval(progressInterval)
            setProgress(100)

            // Store chart data and navigate
            setChartData({
                ...response.data,
                birthDetails: formData
            })

            setTimeout(() => {
                navigate('/charts')
            }, 500)

        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to calculate chart. Make sure the backend is running!')
            setProgress(0)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="page-home">
            <div className="container home-container">
                <div className="home-content">
                    <div className="home-image">
                        <img
                            src="/cosmic-ai.jpg"
                            alt="AI Astrology"
                            className="astro-hero-image"
                            onError={(e) => {
                                e.target.style.display = 'none';
                                e.target.nextElementSibling.style.background = 'radial-gradient(circle, rgba(168, 85, 247, 0.4), transparent 40%), radial-gradient(circle, rgba(0, 245, 255, 0.3), transparent 40%), linear-gradient(135deg, #1a1a2e 0%, #0f172a 50%, #1e293b 100%)';
                                e.target.nextElementSibling.style.height = '500px';
                            }}
                        />
                        <div className="image-overlay">
                            <h2 className="hero-title">Discover Your Cosmic Path</h2>
                            <p className="hero-subtitle">AI-Powered Vedic Insights</p>
                        </div>
                    </div>

                    <div className="home-form">
                        <div className="form-card">
                            <h2>Enter Birth Details</h2>
                            <p className="form-subtitle">Accurate birth information is essential for precise Vedic predictions</p>

                            <form onSubmit={handleSubmit}>
                                <div className="form-group">
                                    <label htmlFor="name">Full Name</label>
                                    <input
                                        type="text"
                                        id="name"
                                        name="name"
                                        value={formData.name}
                                        onChange={handleChange}
                                        required
                                        placeholder="Enter your full name"
                                    />
                                </div>

                                <div className="form-row">
                                    <div className="form-group">
                                        <label htmlFor="date_of_birth">Date of Birth</label>
                                        <input
                                            type="date"
                                            id="date_of_birth"
                                            name="date_of_birth"
                                            value={formData.date_of_birth}
                                            onChange={handleChange}
                                            required
                                        />
                                    </div>

                                    <div className="form-group">
                                        <label htmlFor="time_of_birth">Time of Birth</label>
                                        <input
                                            type="time"
                                            id="time_of_birth"
                                            name="time_of_birth"
                                            value={formData.time_of_birth}
                                            onChange={handleChange}
                                            required
                                            step="1"
                                        />
                                    </div>
                                </div>

                                <div className="form-group autocomplete-wrapper" ref={suggestionsRef}>
                                    <label htmlFor="place_of_birth">
                                        Place of Birth
                                        {searchingPlaces && <span className="searching"> (searching...)</span>}
                                    </label>
                                    <input
                                        type="text"
                                        id="place_of_birth"
                                        name="place_of_birth"
                                        value={formData.place_of_birth}
                                        onChange={handleChange}
                                        onFocus={() => placeSuggestions.length > 0 && setShowSuggestions(true)}
                                        required
                                        placeholder="Type at least 3 characters (e.g., Mumbai)"
                                        autoComplete="off"
                                    />

                                    {showSuggestions && placeSuggestions.length > 0 && (
                                        <ul className="suggestions-list">
                                            {placeSuggestions.map((place, idx) => (
                                                <li
                                                    key={idx}
                                                    onClick={() => handlePlaceSelect(place)}
                                                    className="suggestion-item"
                                                >
                                                    <span className="place-icon">📍</span>
                                                    <span className="place-name">{place.display_name}</span>
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>

                                {loading && (
                                    <div className="progress-container">
                                        <div className="progress-bar">
                                            <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                                        </div>
                                        <p className="progress-text">Calculating charts... {progress}%</p>
                                    </div>
                                )}

                                <button type="submit" disabled={loading} className="submit-btn">
                                    {loading ? 'Calculating...' : 'Calculate Charts'}
                                </button>
                            </form>

                            {error && (
                                <div className="error-message">
                                    <span className="error-icon">❌</span>
                                    <span>{error}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default BirthDetailsForm
