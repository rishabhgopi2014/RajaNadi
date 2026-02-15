import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

const PREDICTION_CATEGORIES = [
    { id: 'marriage', icon: '💑', title: 'Marriage & Relationships', color: '#ec4899' },
    { id: 'career', icon: '💼', title: 'Career & Profession', color: '#8b5cf6' },
    { id: 'health', icon: '🏥', title: 'Health & Wellness', color: '#10b981' },
    { id: 'education', icon: '📚', title: 'Education & Learning', color: '#3b82f6' },
    { id: 'parents', icon: '👨‍👩‍👦', title: 'Parents & Family', color: '#f59e0b' },
    { id: 'children', icon: '👶', title: 'Children & Progeny', color: '#06b6d4' },
    { id: 'wealth', icon: '💰', title: 'Wealth & Finance', color: '#eab308' },
]


function PredictionsPage({ chartData }) {
    const navigate = useNavigate()
    const [activeTab, setActiveTab] = useState('categories')
    const [selectedCategory, setSelectedCategory] = useState(null)
    const [prediction, setPrediction] = useState(null)
    const [loading, setLoading] = useState(false)
    const [customQuestion, setCustomQuestion] = useState('')
    const [progress, setProgress] = useState(0)

    const generatePrediction = async (category, question = null) => {
        setLoading(true)
        setPrediction(null)
        setProgress(0)
        setSelectedCategory(category)

        try {
            const progressInterval = setInterval(() => {
                setProgress(prev => Math.min(prev + 5, 90))
            }, 800)

            const response = await axios.post(`${API_BASE_URL}/generate-prediction`, {
                name: chartData.birthDetails.name,
                natal_chart: chartData.natal,
                navamsa_chart: chartData.navamsa,
                authority_planet: chartData.authority_planet,
                current_transits: chartData.sign_changes || {},
                category: category || 'general',
                custom_question: question,
                // Include birth details for age calculation
                date_of_birth: chartData.birthDetails.date_of_birth,
                time_of_birth: chartData.birthDetails.time_of_birth,
                place_of_birth: chartData.birthDetails.place_of_birth
            })


            clearInterval(progressInterval)
            setProgress(100)
            setPrediction(response.data.prediction_text)

        } catch (err) {
            console.error('Prediction error:', err)
            setPrediction('Error generating prediction. Please try again.')
        } finally {
            setLoading(false)
            setTimeout(() => setProgress(0), 1000)
        }
    }

    const handleCustomQuestion = () => {
        if (customQuestion.trim()) {
            generatePrediction('custom', customQuestion)
        }
    }

    return (
        <div className="page-predictions">
            <div className="container">
                <div className="page-header">
                    <button onClick={() => navigate('/charts')} className="back-btn">← Charts</button>
                    <h2>🔮 Predictions for {chartData.birthDetails.name}</h2>
                </div>

                <div className="tabs-container">
                    <button
                        className={`tab-btn ${activeTab === 'categories' ? 'active' : ''}`}
                        onClick={() => setActiveTab('categories')}
                    >
                        Prediction Categories
                    </button>
                    <button
                        className={`tab-btn ${activeTab === 'custom' ? 'active' : ''}`}
                        onClick={() => setActiveTab('custom')}
                    >
                        Ask Custom Question
                    </button>
                </div>

                {activeTab === 'categories' && (
                    <div className="categories-grid">
                        {PREDICTION_CATEGORIES.map(cat => (
                            <button
                                key={cat.id}
                                className="category-card"
                                style={{ borderColor: cat.color }}
                                onClick={() => generatePrediction(cat.id)}
                                disabled={loading}
                            >
                                <span className="category-icon">{cat.icon}</span>
                                <h3 className="category-title">{cat.title}</h3>
                                <p className="category-desc">Get detailed predictions</p>
                            </button>
                        ))}
                    </div>
                )}

                {activeTab === 'custom' && (
                    <div className="custom-question-section">
                        <h3>Ask Any Specific Question</h3>
                        <textarea
                            className="custom-question-input"
                            value={customQuestion}
                            onChange={(e) => setCustomQuestion(e.target.value)}
                            placeholder="E.g., When will I get promoted? Will I travel abroad? Is this a good time for investment?"
                            rows="4"
                        />
                        <button
                            className="primary-btn"
                            onClick={handleCustomQuestion}
                            disabled={loading || !customQuestion.trim()}
                        >
                            {loading ? 'Generating...' : 'Get Answer'}
                        </button>
                    </div>
                )}

                {loading && (
                    <div className="prediction-loading">
                        <div className="spinner"></div>
                        <div className="progress-container">
                            <div className="progress-bar">
                                <div className="progress-fill" style={{ width: `${progress}%` }}></div>
                            </div>
                            <p className="progress-text">
                                {selectedCategory === 'custom'
                                    ? 'Analyzing your question...'
                                    : `Generating ${PREDICTION_CATEGORIES.find(c => c.id === selectedCategory)?.title} prediction...`
                                } {progress}%
                            </p>
                        </div>
                    </div>
                )}

                {prediction && !loading && (
                    <div className="prediction-result">
                        <div className="prediction-header">
                            <h3>
                                {selectedCategory === 'custom' ? '📖 Your Answer' :
                                    `${PREDICTION_CATEGORIES.find(c => c.id === selectedCategory)?.icon} ${PREDICTION_CATEGORIES.find(c => c.id === selectedCategory)?.title}`
                                }
                            </h3>
                            <button onClick={() => setPrediction(null)} className="close-btn">✕</button>
                        </div>
                        <div className="prediction-content">
                            {prediction.split('\n').map((line, idx) => (
                                <p key={idx}>{line}</p>
                            ))}
                        </div>
                        <button
                            className="secondary-btn"
                            onClick={() => {
                                setPrediction(null)
                                setSelectedCategory(null)
                            }}
                        >
                            Ask Another Question
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}

export default PredictionsPage
