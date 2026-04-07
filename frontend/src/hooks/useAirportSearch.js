import { useEffect, useState } from "react";


export function useAirportSearch() {
    const [searchQuery, setSearchQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState([])

    useEffect(() => {
        if (searchQuery.trim().length < 2) {
            setResults([])
            return
        }
        async function searchAirport() {
            setLoading(true)
            try {
                const data = [] // get all airports from context
                // Normalise to flat shape
                setResults(data.map(a => ({
                    id: a.airport_key,
                    name: a.name,
                    city: a.city?.name ?? a.city_key,
                    country: a.city?.country?.name ?? '',
                    latitude: a.latitude,
                    longitude: a.longitude,
                    tier: a.tier,
                })))
            } catch (err) {
                console.error(err)
                setResults([])
            } finally {
                setLoading(false)
            }
        }
        searchAirport()

    }, [searchQuery])

    return { searchQuery, setSearchQuery, results, loading }
}