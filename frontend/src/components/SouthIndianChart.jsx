import React from 'react'

function SouthIndianChart({ chartData, birthDetails, title }) {
    // South Indian chart layout - Rectangular format
    // 4 rows x 4 columns grid where center shows birth details
    // House positions in South Indian style
    const housePositions = {
        12: { row: 0, col: 0 },
        1: { row: 0, col: 1 },
        2: { row: 0, col: 2 },
        3: { row: 0, col: 3 },
        4: { row: 1, col: 3 },
        5: { row: 2, col: 3 },
        6: { row: 3, col: 3 },
        7: { row: 3, col: 2 },
        8: { row: 3, col: 1 },
        9: { row: 3, col: 0 },
        10: { row: 2, col: 0 },
        11: { row: 1, col: 0 }
    }

    // Group planets by house/rasi
    const planetsByHouse = {}
    Object.entries(chartData).forEach(([planet, data]) => {
        const house = data.rasi
        if (!planetsByHouse[house]) {
            planetsByHouse[house] = []
        }
        // Use short planet names
        const planetNames = {
            'Sun': 'Su',
            'Moon': 'Mo',
            'Mars': 'Ma',
            'Mercury': 'Me',
            'Jupiter': 'Ju',
            'Venus': 'Ve',
            'Saturn': 'Sa',
            'Rahu': 'Ra',
            'Ketu': 'Ke',
            'Ascendant': 'As'
        }
        const shortName = planetNames[planet] || planet.substring(0, 2)
        const retrograde = data.is_retrograde ? '℞' : ''
        planetsByHouse[house].push(`${shortName}${retrograde}`)
    })

    // Create 4x4 grid
    const grid = []
    for (let row = 0; row < 4; row++) {
        const rowCells = []
        for (let col = 0; col < 4; col++) {
            // Check if this is center cell (birth details)
            if ((row === 1 || row === 2) && (col === 1 || col === 2)) {
                if (row === 1 && col === 1) {
                    // Only render birth details once in top-left of center
                    rowCells.push({ type: 'birth', rowSpan: 2, colSpan: 2 })
                } else {
                    rowCells.push({ type: 'skip' })
                }
            } else {
                // Find which house number this position represents
                let houseNum = null
                for (const [house, pos] of Object.entries(housePositions)) {
                    if (pos.row === row && pos.col === col) {
                        houseNum = parseInt(house)
                        break
                    }
                }
                rowCells.push({ type: 'house', houseNum, row, col })
            }
        }
        grid.push(rowCells)
    }

    const renderCell = (cell, rowIdx, colIdx) => {
        if (cell.type === 'skip') return null

        if (cell.type === 'birth') {
            return (
                <div
                    key={`birth-${rowIdx}-${colIdx}`}
                    className="si-birth-cell"
                    style={{ gridRow: `span 2`, gridColumn: `span 2` }}
                >
                    <div className="birth-info">
                        <div className="birth-date">{birthDetails?.date}</div>
                        <div className="birth-time">{birthDetails?.time}</div>
                        <div className="birth-place">{birthDetails?.place}</div>
                    </div>
                </div>
            )
        }

        if (cell.type === 'house') {
            const planets = planetsByHouse[cell.houseNum] || []
            const isAscendant = chartData.Ascendant?.rasi === cell.houseNum

            return (
                <div
                    key={`house-${rowIdx}-${colIdx}`}
                    className={`si-house-cell ${isAscendant ? 'ascendant' : ''}`}
                >
                    <div className="house-number">{cell.houseNum}</div>
                    <div className="house-planets">
                        {planets.map((p, idx) => (
                            <span key={idx} className="planet-text">{p}</span>
                        ))}
                    </div>
                </div>
            )
        }

        return null
    }

    return (
        <div className="south-indian-chart">
            <h4 className="chart-title">{title}</h4>
            <div className="si-chart-grid">
                {grid.map((row, rowIdx) =>
                    row.map((cell, colIdx) => renderCell(cell, rowIdx, colIdx))
                )}
            </div>

            <div className="chart-legend">
                <div className="legend-item">
                    <span className="legend-label">Su=Sun, Mo=Moon, Ma=Mars, Me=Mercury</span>
                </div>
                <div className="legend-item">
                    <span className="legend-label">Ju=Jupiter, Ve=Venus, Sa=Saturn</span>
                </div>
                <div className="legend-item">
                    <span className="legend-label">Ra=Rahu, Ke=Ketu, As=Ascendant</span>
                </div>
            </div>
        </div>
    )
}

export default SouthIndianChart
