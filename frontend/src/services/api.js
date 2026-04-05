
const BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://127.0.0.1:8000'

async function request(method, path, body){

    let bodyStringified

    if (body){
        bodyStringified = { body: JSON.stringify(body)}
    }

    const res = await fetch(`${BASE_URL}${path}`, {
        method,
        headers: {'Content-Type': 'application/json'},
        ...bodyStringified
    })
    
    if (!res.ok) {

        let message = `API error: ${res.status}`
        try{
            const error = await res.json()
            if (error.detail){
                message = error.detail
                message = Array.isArray(message) ? message[0]?.msg ?? "Unknown Error Format" : message;
                console.log(error.detail)
            } 
        } catch (e){} // Keep default message        
        throw new Error(message)    
    }
    // const data = await res.json()
    // return data
    // anyway the calling function will be using await as this is an async function
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

export const authAPI = {
    login: (creds) => request('POST', '/user/login', creds),
    register: (creds) => request('POST', '/user', creds),
    logout: null
}

export const tripAPI = {
    save : (trip) => request('POST', '/trip', trip),
    getAll: (userId) => request('GET', `/${userId}/trips` ), 
    delete: (tripId) => request('DELETE', `/trip/${tripId}` )
}