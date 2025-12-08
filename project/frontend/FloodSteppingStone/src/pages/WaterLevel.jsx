import { useState, useEffect, useRef } from 'react'
import Footer from '../components/Footer'
import '../styles/WaterLevel.css'
import { fetchCurrentStatus, createNotification, MOCK_MODE } from '../api/waterLevelApi'

function WaterLevel() {
    const [sensor1Active, setSensor1Active] = useState(false)
    const [sensor2Active, setSensor2Active] = useState(false)
    const [bothSensorsStartTime, setBothSensorsStartTime] = useState(null)
    const bothSensorsTimeoutRef = useRef(null)
    const [currentStage, setCurrentStage] = useState(0) // 현재 수위 단계 (0, 1, 2, 3)

    // currentStage 변경 시 로그
    useEffect(() => {
        console.log('🌊 현재 수위 단계 변경됨:', currentStage)
        console.log('📸 표시될 이미지:', `water-level${currentStage}.png`)
    }, [currentStage])

    // 새로고침 시에만 알림 초기화
    useEffect(() => {
        if (MOCK_MODE) {
            // performance.navigation.type으로 새로고침 감지
            // 또는 performance.getEntriesByType('navigation')[0].type 사용
            const navEntries = performance.getEntriesByType('navigation')
            const isReload = navEntries.length > 0 && navEntries[0].type === 'reload'

            if (isReload) {
                // 새로고침인 경우에만 초기화
                localStorage.removeItem('notifications')
                localStorage.removeItem('lastReadTime')
            }
        }
    }, [])

    // 현재 수위 단계 조회 (API 호출)
    useEffect(() => {
        const getCurrentStatus = async () => {
            if (MOCK_MODE) {
                // Mock 모드에서는 센서 상태에 따라 stage 계산
                if (sensor1Active && sensor2Active) {
                    setCurrentStage(3)
                } else if (sensor2Active) {
                    setCurrentStage(2)
                } else if (sensor1Active) {
                    setCurrentStage(1)
                } else {
                    setCurrentStage(0)
                }
                return
            }

            // 실제 API 호출
            const data = await fetchCurrentStatus()
            setCurrentStage(data.stage || 0)
        }

        // 초기 데이터 가져오기
        getCurrentStatus()

        if (!MOCK_MODE) {
            // 실제 모드에서는 2초마다 상태 폴링
            const interval = setInterval(getCurrentStatus, 2000)
            return () => clearInterval(interval)
        }
    }, [sensor1Active, sensor2Active])


    // 센서 상태에 따른 알림 생성
    useEffect(() => {
        // 센서 1만 감지된 경우
        if (sensor1Active && !sensor2Active) {
            createNotification(1)
        }

        // 센서 2가 감지된 경우
        if (sensor2Active) {
            createNotification(2)
        }

        // 두 센서 모두 감지된 경우 - 5초 타이머 시작
        if (sensor1Active && sensor2Active) {
            if (!bothSensorsStartTime) {
                setBothSensorsStartTime(Date.now())

                // 5초 후 경고 알림
                bothSensorsTimeoutRef.current = setTimeout(async () => {
                    await createNotification(3)
                }, 5000)
            }
        } else {
            // 센서 중 하나라도 비활성화되면 타이머 초기화
            if (bothSensorsTimeoutRef.current) {
                clearTimeout(bothSensorsTimeoutRef.current)
                bothSensorsTimeoutRef.current = null
            }
            setBothSensorsStartTime(null)
        }

        return () => {
            if (bothSensorsTimeoutRef.current) {
                clearTimeout(bothSensorsTimeoutRef.current)
            }
        }
    }, [sensor1Active, sensor2Active, bothSensorsStartTime])


    return (
        <>
            <h1 className="Page-Title">
                <span className="highlight-gray">현재 내 차 </span>
                <span className="highlight-blue"> 수위</span>
            </h1>

            <div className="water-level-image-container">
                <img
                    src={`/water-level${currentStage}.png`}
                    className="water-level-image"
                    alt={`수위 단계 ${currentStage}`}
                />
            </div>

            {/* 수위 단계별 경고 메시지 */}
            <div className="warning-message-container">
                {currentStage === 0 && (
                    <div className="warning-message safe">
                        <span className="warning-icon">🍀</span>
                        <p className="warning-text">현재 물이 감지되지 않았습니다.</p>
                    </div>
                )}
                {currentStage === 1 && (
                    <div className="warning-message warning">
                        <span className="warning-icon">⚠️</span>
                        <p className="warning-text">경고! 물이 감지되었습니다!</p>
                    </div>
                )}
                {currentStage === 2 && (
                    <div className="warning-message danger">
                        <span className="warning-icon">🚨</span>
                        <p className="warning-text">경고! 바퀴까지 물이 차올랐습니다.<br />안전벨트를 풀고 탈출을 준비하십시오!</p>
                    </div>
                )}
                {currentStage === 3 && (
                    <div className="warning-message critical">
                        <span className="warning-icon">🚨</span>
                        <p className="warning-text">탈출하세요! 5초간 물이 감지되어<br />창문이 자동으로 열립니다!</p>
                    </div>
                )}
            </div>

            {/* Mock 모드 테스트 버튼 */}
            {MOCK_MODE && (
                <div style={{
                    textAlign: 'center',
                    marginTop: '20px',
                    display: 'flex',
                    gap: '10px',
                    justifyContent: 'center',
                    flexWrap: 'wrap',
                    padding: '0 20px'
                }}>
                    <button
                        onClick={() => setSensor1Active(!sensor1Active)}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: sensor1Active ? '#FF4444' : '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontSize: '14px'
                        }}
                    >
                        센서 1 {sensor1Active ? 'OFF' : 'ON'}
                    </button>
                    <button
                        onClick={() => setSensor2Active(!sensor2Active)}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: sensor2Active ? '#FF4444' : '#4CAF50',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontSize: '14px'
                        }}
                    >
                        센서 2 {sensor2Active ? 'OFF' : 'ON'}
                    </button>
                    <button
                        onClick={() => {
                            setSensor1Active(false)
                            setSensor2Active(false)
                        }}
                        style={{
                            padding: '10px 20px',
                            backgroundColor: '#808080',
                            color: 'white',
                            border: 'none',
                            borderRadius: '8px',
                            cursor: 'pointer',
                            fontSize: '14px'
                        }}
                    >
                        모두 OFF
                    </button>
                </div>
            )}

            <Footer currentPage="water-level" />
        </>
    )
}

export default WaterLevel
