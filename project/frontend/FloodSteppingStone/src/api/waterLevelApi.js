const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MOCK_MODE = import.meta.env.VITE_MOCK_MODE === 'true'

/**
 * 현재 수위 상태 조회 API
 * @returns {Promise<{stage: number}>}
 */
export const fetchCurrentStatus = async () => {
    if (MOCK_MODE) {
        // Mock 모드에서는 기본값 반환
        return { stage: 0 }
    }

    try {
        const response = await fetch(`${API_BASE_URL}/status/current`)

        if (!response.ok) {
            throw new Error('상태 조회 실패')
        }

        const data = await response.json()
        console.log('API 응답 데이터:', data)
        console.log('현재 stage:', data.stage)

        return data
    } catch (error) {
        console.error('현재 상태를 가져오는데 실패했습니다:', error)
        // API 호출 실패 시 기본값 반환
        return { stage: 0 }
    }
}

/**
 * 알림 생성 API
 * @param {number} stage - 수위 단계 (1, 2, 3)
 * @returns {Promise<void>}
 */
export const createNotification = async (stage) => {
    if (MOCK_MODE) {
        // Mock 모드: localStorage에 알림 저장
        const notifications = JSON.parse(localStorage.getItem('notifications') || '[]')
        const newNotification = {
            log_id: Date.now(),
            stage: stage,
            status: stage === 3 ? 'critical' : 'warning',
            created_at: new Date().toISOString()
        }
        notifications.unshift(newNotification) // 최신 알림을 맨 위에
        localStorage.setItem('notifications', JSON.stringify(notifications))
        console.log('알림 생성:', newNotification)
        return Promise.resolve(newNotification)
    }

    try {
        const response = await fetch(`${API_BASE_URL}/sensor/logs`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                sensor_id: stage === 1 ? 1 : 2,
                stage: stage,
                recorded_at: new Date().toISOString(),
            }),
        })

        if (!response.ok) {
            throw new Error('알림 생성 실패')
        }

        return await response.json()
    } catch (error) {
        console.error('알림 생성 실패:', error)
        throw error
    }
}

export { MOCK_MODE }
