import { useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import '../styles/footer.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'
const MOCK_MODE = import.meta.env.VITE_MOCK_MODE === 'true'

function Footer({ currentPage }) {
    const navigate = useNavigate()
    const [unreadCount, setUnreadCount] = useState(0)

    // 읽지 않은 알림 개수 계산
    useEffect(() => {
        const checkUnreadNotifications = async () => {
            const lastReadLogId = parseInt(localStorage.getItem('lastReadLogId') || '0', 10)

            if (MOCK_MODE) {
                const notifications = JSON.parse(localStorage.getItem('notifications') || '[]')
                const latestLogId = notifications.reduce(
                    (max, n) => Math.max(max, n.log_id ?? 0),
                    lastReadLogId
                )
                localStorage.setItem('latestLogId', String(latestLogId))
                const unread = notifications.filter(n => (n.log_id ?? 0) > lastReadLogId).length
                setUnreadCount(unread)
                return
            }

            try {
                const response = await fetch(`${API_BASE_URL}/notifications`)
                if (!response.ok) {
                    throw new Error('알림 조회 실패')
                }
                const data = await response.json()
                const latestLogId = data.reduce(
                    (max, n) => Math.max(max, n.log_id ?? 0),
                    lastReadLogId
                )
                localStorage.setItem('latestLogId', String(latestLogId))
                const unread = data.filter(n => (n.log_id ?? 0) > lastReadLogId).length
                setUnreadCount(unread)
            } catch (error) {
                console.error('알림 개수 조회 실패:', error)
            }
        }

        checkUnreadNotifications()
        const interval = setInterval(checkUnreadNotifications, 2000)
        return () => clearInterval(interval)
    }, [])

    const handleCarClick = () => {
        if (currentPage === 'water-level') {
            navigate('/')
        } else {
            navigate('/water-level')
        }
    }

    const handleBellClick = () => {
        const latestLogId = localStorage.getItem('latestLogId') || '0'
        localStorage.setItem('lastReadLogId', latestLogId)
        navigate('/water-level-notification')
    }

    const handleSettingClick = () => {
        if (currentPage !== 'setting') {
            navigate('/setting')
        }
    }

    const handleHomeClick = () => {
        if (currentPage !== 'home') {
            navigate('/')
        }
    }

    return (
        <footer className="footer-container">
            <img
                className={currentPage === 'water-level' ? 'Car-On' : 'Car-Off'}
                src={currentPage === 'water-level' ? '/Car-On.svg' : '/Car-Off.svg'}
                onClick={handleCarClick}
            />
            <div className="bell-wrapper">
                <img className="Bell-Off" src="/Bell-Off.svg" onClick={handleBellClick} />
                {unreadCount > 0 && (
                    <div className="notification-badge">
                        {unreadCount >= 5 ? '5+' : unreadCount}
                    </div>
                )}
            </div>
            <img
                className={currentPage === 'setting' ? 'Setting-On' : 'Setting-Off'}
                src={currentPage === 'setting' ? '/Setting-On.svg' : '/Setting-Off.svg'}
                onClick={currentPage === 'setting' ? handleHomeClick : handleSettingClick}
            />
        </footer>
    )
}

export default Footer
