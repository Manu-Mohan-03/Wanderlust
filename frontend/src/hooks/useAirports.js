
import { useState, useEffect } from 'react'
import { airportAPI } from '../services/api'

// Normalise raw API response to a flat shape MapView needs
function normalise(raw) {
    return {
        id: raw.airport_key,
        name: raw.name,
        city: raw.city?.name ?? raw.city_key,
        country: raw.city?.country?.name ?? raw.city?.country_key ?? '',
        latitude: raw.latitude,
        longitude: raw.longitude,
        tier: raw.tier,
    }
}

export function useAirports() {
    const [airports, setAirports] = useState([])   // all tier-1 airports
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        async function getAirports() {
            try {
                const data = await airportAPI.getAll()
                const tier1 = data
                    .filter(airport => airport.tier === 1)
                    .map(normalise)
                setAirports(tier1)
                
            } catch (err) {
                setError('Failed to load airports')
                console.error(err)
            } finally {
                setLoading(false)
            }
        }
        getAirports()
    }, [])

    return { airports, airportsloading: loading, error }
}

/* Sample API Data 
    "airport_key": "CGN",
    "name": "Cologne/bonn",
    "city_key": "CGN",
    "latitude": 50.878365,
    "longitude": 7.122224,
    "city": {
        "name": "Cologne",
        "country_key": "DE",
        "timezone": "Europe/Berlin",
        "country": {
            "country_key": "DE",
            "name": "Germany"
        }
    }
*/