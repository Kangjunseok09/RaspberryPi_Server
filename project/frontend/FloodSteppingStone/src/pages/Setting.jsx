import { useState, useEffect } from 'react'
import Footer from '../components/Footer'
import '../styles/Setting.css'

function Setting() {
    const [selectedLevel, setSelectedLevel] = useState(1) // 현재 선택된 단계
    const [level1Color, setLevel1Color] = useState('#6BCF7F') // 1단계 초록
    const [level2Color, setLevel2Color] = useState('#FFD93D') // 2단계 노랑
    const [level3Color, setLevel3Color] = useState('#FF6B6B') // 3단계 빨강
    const [buzzerVolume, setBuzzerVolume] = useState(50)

    const lightColors = [
        { name: '파랑', color: '#75A1E7' },
        { name: '빨강', color: '#FF6B6B' },
        { name: '노랑', color: '#FFD93D' },
        { name: '초록', color: '#6BCF7F' },
        { name: '보라', color: '#9B59B6' },
        { name: '주황', color: '#FF8C42' },
    ]

    // localStorage에서 설정 불러오기
    useEffect(() => {
        const savedLevel1Color = localStorage.getItem('level1Color')
        const savedLevel2Color = localStorage.getItem('level2Color')
        const savedLevel3Color = localStorage.getItem('level3Color')
        const savedVolume = localStorage.getItem('buzzerVolume')

        if (savedLevel1Color) setLevel1Color(savedLevel1Color)
        if (savedLevel2Color) setLevel2Color(savedLevel2Color)
        if (savedLevel3Color) setLevel3Color(savedLevel3Color)
        if (savedVolume) setBuzzerVolume(parseInt(savedVolume))
    }, [])

    // 단계별 조명 색상 변경
    const handleLevel1ColorChange = (color) => {
        setLevel1Color(color)
        localStorage.setItem('level1Color', color)
    }

    const handleLevel2ColorChange = (color) => {
        setLevel2Color(color)
        localStorage.setItem('level2Color', color)
    }

    const handleLevel3ColorChange = (color) => {
        setLevel3Color(color)
        localStorage.setItem('level3Color', color)
    }

    // 부저 볼륨 변경
    const handleVolumeChange = (volume) => {
        setBuzzerVolume(volume)
        localStorage.setItem('buzzerVolume', volume.toString())
    }


    // 현재 선택된 단계의 색상 가져오기
    const getCurrentColor = () => {
        if (selectedLevel === 1) return level1Color
        if (selectedLevel === 2) return level2Color
        return level3Color
    }

    // 현재 선택된 단계의 색상 변경 핸들러 가져오기
    const getCurrentColorHandler = () => {
        if (selectedLevel === 1) return handleLevel1ColorChange
        if (selectedLevel === 2) return handleLevel2ColorChange
        return handleLevel3ColorChange
    }

    return (
        <>
            <h1 className="Page-Title">
                <span className="highlight-blue">설정</span>
            </h1>

            <div className="setting-container">
                <div className="setting-section">
                    <h2 className="setting-section-title">조명 색상 변경</h2>

                    {/* 단계 선택 버튼 */}
                    <div className="level-selector">
                        <button
                            className={`level-button ${selectedLevel === 1 ? 'active' : ''}`}
                            onClick={() => setSelectedLevel(1)}
                        >
                            현재등
                        </button>
                        <button
                            className={`level-button ${selectedLevel === 2 ? 'active' : ''}`}
                            onClick={() => setSelectedLevel(2)}
                        >
                            경고등
                        </button>
                        <button
                            className={`level-button ${selectedLevel === 3 ? 'active' : ''}`}
                            onClick={() => setSelectedLevel(3)}
                        >
                            위험등
                        </button>
                    </div>

                    <div className="light-preview">
                        <div
                            className="light-bulb"
                            style={{ backgroundColor: getCurrentColor() }}
                        >
                            <div className="light-glow" style={{ boxShadow: `0 0 60px ${getCurrentColor()}` }}></div>
                        </div>
                        <p className="selected-color-name">
                            현재 선택된 색상: <span style={{ color: getCurrentColor() }}>
                                {lightColors.find(c => c.color === getCurrentColor())?.name || '커스텀'}
                            </span>
                        </p>
                    </div>

                    <div className="color-grid">
                        {lightColors.map((item) => (
                            <div
                                key={item.color}
                                className={`color-option ${getCurrentColor() === item.color ? 'selected' : ''}`}
                                onClick={() => getCurrentColorHandler()(item.color)}
                            >
                                <div
                                    className="color-circle"
                                    style={{ backgroundColor: item.color }}
                                ></div>
                                <span className="color-name">{item.name}</span>
                            </div>
                        ))}
                    </div>

                    <div className="custom-color-section">
                        <label htmlFor="customColor" className="custom-color-label">
                            원하는 색상 직접 선택:
                        </label>
                        <div className="custom-color-input-wrapper">
                            <input
                                id="customColor"
                                type="color"
                                value={getCurrentColor()}
                                onChange={(e) => getCurrentColorHandler()(e.target.value)}
                                className="custom-color-input"
                            />
                            <span className="custom-color-code">{getCurrentColor()}</span>
                        </div>
                    </div>
                </div>
            </div>

            <Footer currentPage="setting" />
        </>
    )
}

export default Setting
