import { useCallback, useState } from 'react'
import { airportAPI } from '../services/api'

// Normalise route to shape ArcLayer needs
function normalise(raw) {
    return {
        flightId: raw.flight_id,
        airline: raw.airline,
        from: {
            id: raw.orig_airport_details.airport_key,
            name: raw.orig_airport_details.name,
            latitude: raw.orig_airport_details.latitude,
            longitude: raw.orig_airport_details.longitude,
        },
        to: {
            id: raw.dest_airport_details.airport_key,
            name: raw.dest_airport_details.name,
            latitude: raw.dest_airport_details.latitude,
            longitude: raw.dest_airport_details.longitude,
        },
    }
}

export function useRoutes() {

    const [routes, setRoutes] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const fetchRoutes = useCallback(async (airportId) => {
        setLoading(true)
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

    return { routes, loading, error, fetchRoutes }

}

