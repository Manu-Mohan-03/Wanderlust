
const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

async function request(method, path){
    const res = await fetch(`${BASE_URL}${path}`, {
        method,
        headers: {'Content-Type': 'application/json'}
    })
    if (!res.ok) throw new Error(`API error: ${res.status}`)    
    // const data = await res.json()
    // return data
    // anyway the calling function will be using await as this is an asnc function
    return res.json() 
}

export const airportAPI = {
    // For all airports
    getAll: () => request('GET', '/airports'), 
    // For routes from a specific airport  // API can handle city instead of airports
    // accepts query parameter mode for Departure(Default)/Arrival), you can set both arrival
    // and destinations(either city or airport), and also date and time
    getRoutes: (iata)=>request('GET', `/flights/${iata}/airport`) 
}