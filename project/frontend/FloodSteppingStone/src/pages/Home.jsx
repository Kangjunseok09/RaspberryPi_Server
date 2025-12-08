import { useState } from 'react'
import Footer from '../components/Footer'
import '../styles/Home.css'
import '../styles/modal.css'
import '../styles/WaterLevel.css'
import '../styles/WaterLevelNotification.css'
import '../styles/Setting.css'

function Home() {
    const [showModal, setShowModal] = useState(true)

    return (
        <>
            {showModal && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <button className="modal-close" onClick={() => setShowModal(false)}>
                            ×
                        </button>
                        <h2>
                            <img className = "Modal-img" src="/Main-Logo.png" />
                            <span className="modal-title-flood">홍수</span>
                            <span className="modal-title-stone">디딤이란?</span>
                        </h2>
                        <div className="modal-description">
                            <p>홍수디딤이는 홍수 상황에서 운전자가 침수에 당황하지 않고 안전하게 대피할 수 있도록 도와주는 서비스입니다.</p>
                            <p>현재 차량의 침수정도를 실시간으로 보여주고, 침수가 빠르게 진행되면 운전자가 인식할 수 있도록 경보음을 울려 탈출을 도와줍니다.</p>
                            <ul>
                                <li>실시간 내 차 수위 확인</li>
                                <li>경보음으로 신속한 대피 가능</li>
                                <li>비상시 자동 창문열림</li>
                            </ul>
                        </div>
                    </div>
                </div>
            )}

            <div className="Main-Title">
                <span>홍수</span>
                <span>디딤이</span>
            </div>

            <div className="Flood-container">
                <div className="Flood-wrapper">
                    <div className="Flood-group">
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />


                    </div>
                    <div className="Flood-group">
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood2.png" alt="Flood" />
                        <img className="Flood-image" src="/Flood1.png" alt="Flood" />
                    </div>
                </div>
            </div>

            <Footer currentPage="home" />
        </>
    )
}
export default Home
