const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

export const fetchLedColors = async () => {
    const response = await fetch(`${API_BASE_URL}/led/colors`)
    if (!response.ok) {
        throw new Error('LED 색상 조회 실패')
    }
    const data = await response.json()
    const mapped = {}
    data.forEach((item) => {
        mapped[item.state] = item.color_hex
    })
    return mapped
}

export const updateLedColor = async (state, colorHex) => {
    const response = await fetch(`${API_BASE_URL}/led/colors/${state}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ color_hex: colorHex }),
    })
    if (!response.ok) {
        throw new Error('LED 색상 저장 실패')
    }
    return response.json()
}
