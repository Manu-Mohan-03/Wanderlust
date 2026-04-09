import { useCallback, useState } from 'react'
import { airportAPI } from '../services/api'

// Normalise route to shape ArcLayer needs
function normalise(raw) {
    return {
        flightId: raw.flight_id,
        airline: raw.airline,
        from: {
            id: raw.orig_airport,
            name: raw.orig_airport_details.name,
            city: raw.orig_airport_details.city.name,  // Added to include city details
            latitude: raw.orig_airport_details.latitude,
            longitude: raw.orig_airport_details.longitude,
            country: raw.orig_airport_details.city.country.country_key
        },
        to: {
            id: raw.dest_airport,
            name: raw.dest_airport_details.name,
            city: raw.dest_airport_details.city.name, // Added to include city details
            latitude: raw.dest_airport_details.latitude,
            longitude: raw.dest_airport_details.longitude,
            country: raw.dest_airport_details.city.country.country_key
        },
    }
}

export function useRoutes() {

    const [routes, setRoutes] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const fetchRoutes = useCallback(async (airportId) => {
        setLoading(true)
        setError(null)
        try {
            const data = await airportAPI.getRoutes(airportId)
            setRoutes(data.filter(r => r.status === 'active').map(normalise))
        } catch (err) {
            setError('Failed to load routes')
            console.error(err)
        } finally {
            setLoading(false)
        }
    }, [])

    const clearRoutes = () => setRoutes([])

    return { routes, loading, error, fetchRoutes, clearRoutes }

}

