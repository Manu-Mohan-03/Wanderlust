
const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

async function request(method, path){
    const res = await fetch(`${BASE_URL}${path}`, {
        method,
        headers: {'Content-Type': 'application/json'}
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)    
    const data = await res.json()
    return data
}

export const airportAPI = {
    getAll: () => request('GET', '/airports')
}