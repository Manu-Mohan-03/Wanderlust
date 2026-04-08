import { useContext, useEffect, useState } from "react";
import { TripDetails } from "../context/TripContext";
import { filterAirports } from "../services/search";


export function useAirportSearch() {
    const [searchQuery, setSearchQuery] = useState('')
    const [loading, setLoading] = useState(false)
    const [results, setResults] = useState([])
    const { allAirports } = useContext(TripDetails)

    useEffect(() => {
        if (searchQuery.trim().length < 2) {
            setResults([])
            return
        }
        function searchAirport() {
            setLoading(true)
            try {
                // const data = allAirports
                // Normalise to flat shape
                const searchResults = filterAirports(allAirports, searchQuery)
                setResults(searchResults)
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