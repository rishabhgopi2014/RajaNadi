import { useNavigate } from 'react-router-dom'
import SouthIndianChart from './SouthIndianChart'

// Nakshatra names (27 nakshatras)
const NAKSHATRAS = [
    'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
    'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
    'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
    'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
    'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
]

// Calculate Nakshatra from longitude (0-360 degrees)
function getNakshatraName(longitude) {
    // Each nakshatra is 13.333... degrees (360 / 27)
    const nakshatraDegrees = 360 / 27
    const nakshatraIndex = Math.floor(longitude / nakshatraDegrees)
    return NAKSHATRAS[nakshatraIndex] || 'Unknown'
}

// Calculate Pada (1-4) within a Nakshatra
function getNakshatraPada(longitude) {
    const nakshatraDegrees = 360 / 27  // 13.333...
    const positionInNakshatra = longitude % nakshatraDegrees
    const pada = Math.floor(positionInNakshatra / (nakshatraDegrees / 4)) + 1
    return pada
}

function ChartsPage({ chartData }) {
    const navigate = useNavigate()

    return (
        <div className="page-charts">
            <div className="container">
                <div className="page-header">
                    <button onClick={() => navigate('/')} className="back-btn">← Back</button>
                    <h2>📊 Astrological Charts for {chartData.birthDetails.name}</h2>
                </div>

                {/* Rasi and Nakshatra Information Section */}
                <div className="rasi-nakshatra-section">
                    <div className="info-cards-grid">
                        <div className="chart-card highlight-card rasi-card">
                            <h3>🌙 Rasi (Moon Sign)</h3>
                            {chartData.natal.Moon && (
                                <>
                                    <p className="rasi-name-large">{chartData.natal.Moon.rasi_name}</p>
                                    <p className="chart-desc">Rasi {chartData.natal.Moon.rasi}</p>
                                    <p className="rasi-degree">Moon at {chartData.natal.Moon.degree.toFixed(2)}°</p>
                                </>
                            )}
                        </div>

                        <div className="chart-card highlight-card nakshatra-card">
                            <h3>⭐ Nakshatra (Birth Star)</h3>
                            {chartData.natal.Moon && (
                                <>
                                    <p className="nakshatra-name-large">{getNakshatraName(chartData.natal.Moon.longitude)}</p>
                                    <p className="chart-desc">Pada {getNakshatraPada(chartData.natal.Moon.longitude)}</p>
                                    <p className="nakshatra-degree">Based on Moon's longitude {chartData.natal.Moon.longitude.toFixed(2)}°</p>
                                </>
                            )}
                        </div>

                        <div className="chart-card highlight-card ascendant-info-card">
                            <h3>🔺 Ascendant (Lagna)</h3>
                            {chartData.natal.Ascendant && (
                                <>
                                    <p className="rasi-name-large">{chartData.natal.Ascendant.rasi_name}</p>
                                    <p className="chart-desc">Rasi {chartData.natal.Ascendant.rasi}</p>
                                    <p className="rasi-degree">At {chartData.natal.Ascendant.degree.toFixed(2)}°</p>
                                </>
                            )}
                        </div>
                    </div>
                </div>

                <div className="charts-visual-container">
                    <div className="chart-visual-card">
                        <SouthIndianChart
                            chartData={chartData.natal}
                            birthDetails={{
                                date: chartData.birthDetails.date_of_birth,
                                time: chartData.birthDetails.time_of_birth,
                                place: chartData.birthDetails.place_of_birth
                            }}
                            title="Natal Chart (D1 - Rasi)"
                        />
                    </div>

                    <div className="chart-visual-card">
                        <SouthIndianChart
                            chartData={chartData.navamsa}
                            birthDetails={{
                                date: chartData.birthDetails.date_of_birth,
                                time: chartData.birthDetails.time_of_birth,
                                place: 'Navamsa (D9)'
                            }}
                            title="Navamsa Chart (D9)"
                        />
                    </div>
                </div>

                {/* Authority Planet and Gemstone side by side */}
                <div className="info-cards-grid">
                    <div className="chart-card highlight-card">
                        <h3>⭐ Authority Planet</h3>
                        <p className="authority-planet-large">{chartData.authority_planet}</p>
                        <p className="chart-desc">The primary planet influencing your life</p>
                    </div>

                    {chartData.lucky_gemstone && (
                        <div className="chart-card gemstone-card">
                            <h3>💎 Lucky Gemstone</h3>
                            <p className="gemstone-name">{chartData.lucky_gemstone.gemstone}</p>
                            <div className="gemstone-details">
                                <p><strong>Ruling Planet:</strong> {chartData.lucky_gemstone.planet}</p>
                                <p><strong>Wear on Finger:</strong> {chartData.lucky_gemstone.finger}</p>
                                <p><strong>Auspicious Day to Wear:</strong> {chartData.lucky_gemstone.day}</p>
                                {chartData.lucky_gemstone.benefits && (
                                    <p className="gemstone-benefits">{chartData.lucky_gemstone.benefits}</p>
                                )}
                                {chartData.lucky_gemstone.mantra && (
                                    <p className="gemstone-mantra">{chartData.lucky_gemstone.mantra}</p>
                                )}
                            </div>
                        </div>
                    )}
                </div>

                {/* Natal and Navamsa Details below */}
                <div className="info-cards-grid">
                    <div className="chart-card">
                        <h3>🌟 Natal Details (D1)</h3>
                        <p className="chart-desc">Birth chart positions</p>

                        <div className="chart-grid">
                            {Object.entries(chartData.natal).map(([planet, data]) => (
                                <div key={planet} className="planet-row">
                                    <span className="planet-name">
                                        {planet}
                                        {data.is_retrograde && <span className="retrograde-badge">R</span>}
                                    </span>
                                    <span className="planet-rasi">{data.rasi_name}</span>
                                    <span className="planet-degree">{data.degree.toFixed(1)}°</span>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="chart-card">
                        <h3>💫 Navamsa Details (D9)</h3>
                        <p className="chart-desc">Divisional chart positions</p>

                        <div className="chart-grid">
                            {Object.entries(chartData.navamsa).map(([planet, data]) => (
                                <div key={planet} className="planet-row">
                                    <span className="planet-name">
                                        {planet}
                                        {data.is_retrograde && <span className="retrograde-badge">R</span>}
                                    </span>
                                    <span className="planet-rasi">{data.rasi_name}</span>
                                    <span className="planet-degree">{data.degree.toFixed(1)}°</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Sign Changes & Retrograde Overview */}
                <div className="transits-section">
                    <h3 className="section-title">🌟 Upcoming Transits for 2026</h3>
                    <p className="section-subtitle">Major planetary movements and retrograde periods</p>

                    {/* Sign Changes */}
                    <div className="sign-changes-container">
                        <div className="planet-sign-section">
                            <h4 className="planet-sign-title">🪐 Jupiter (Guru)</h4>
                            <ul className="sign-change-list">
                                <li>Enters <strong>Cancer</strong> on June 2, 2026 (Exalted)</li>
                                <li>Moves into <strong>Leo</strong> on October 31, 2026</li>
                            </ul>
                        </div>

                        <div className="planet-sign-section">
                            <h4 className="planet-sign-title">🪐 Saturn (Shani)</h4>
                            <ul className="sign-change-list">
                                <li>Remains in <strong>Pisces</strong> for the entirety of 2026</li>
                                <li>Briefly re-enters <strong>Aries</strong> on February 13-14, 2026, before retrograding back</li>
                            </ul>
                        </div>

                        <div className="planet-sign-section">
                            <h4 className="planet-sign-title">🪐 Rahu & Ketu</h4>
                            <ul className="sign-change-list">
                                <li>Stay in the <strong>Aquarius-Leo</strong> axis for most of the year</li>
                                <li>Rahu enters <strong>Capricorn</strong> and Ketu enters <strong>Cancer</strong> on November 25, 2026</li>
                            </ul>
                        </div>

                        <div className="planet-sign-section">
                            <h4 className="planet-sign-title">🪐 Uranus</h4>
                            <ul className="sign-change-list">
                                <li>Re-enters <strong>Gemini</strong> on April 25, 2026</li>
                            </ul>
                        </div>

                        <div className="planet-sign-section">
                            <h4 className="planet-sign-title">🪐 Neptune</h4>
                            <ul className="sign-change-list">
                                <li>Re-enters <strong>Aries</strong> on January 26, 2026</li>
                            </ul>
                        </div>
                    </div>

                    {/* Retrograde Periods Table */}
                    <div className="retrograde-container">
                        <h4 className="retrograde-title">🔄 2026 Retrograde Periods</h4>
                        <p className="retrograde-subtitle">Retrograde motions indicate periods for reflection and re-evaluation</p>

                        <div className="retrograde-table-wrapper">
                            <table className="retrograde-table">
                                <thead>
                                    <tr>
                                        <th>Planet</th>
                                        <th>Retrograde Begins</th>
                                        <th>Retrograde Ends</th>
                                        <th>Sign(s)</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td rowSpan="3" className="planet-cell">Mercury</td>
                                        <td>Feb 26</td>
                                        <td>Mar 20</td>
                                        <td>Pisces</td>
                                    </tr>
                                    <tr>
                                        <td>Jun 29</td>
                                        <td>Jul 24</td>
                                        <td>Cancer/Gemini</td>
                                    </tr>
                                    <tr>
                                        <td>Oct 24</td>
                                        <td>Nov 13</td>
                                        <td>Scorpio/Libra</td>
                                    </tr>
                                    <tr>
                                        <td className="planet-cell">Venus</td>
                                        <td>Oct 3</td>
                                        <td>Nov 14</td>
                                        <td>Scorpio/Libra</td>
                                    </tr>
                                    <tr>
                                        <td rowSpan="2" className="planet-cell">Jupiter</td>
                                        <td>(From 2025)</td>
                                        <td>Mar 11</td>
                                        <td>Cancer</td>
                                    </tr>
                                    <tr>
                                        <td>Dec 13</td>
                                        <td>(Into 2027)</td>
                                        <td>Leo</td>
                                    </tr>
                                    <tr>
                                        <td className="planet-cell">Saturn</td>
                                        <td>Jul 27</td>
                                        <td>Dec 11</td>
                                        <td>Pisces/Aries</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div className="nav-actions">
                    <button
                        onClick={() => navigate('/predictions')}
                        className="primary-btn predictions-btn"
                    >
                        View AI Predictions →
                    </button>
                </div>
            </div>
        </div>
    )
}

export default ChartsPage
