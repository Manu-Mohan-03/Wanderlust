// Handles all the logic of integrating with MapView and SearchInput
import { useContext, useImperativeHandle, useState } from 'react'
import SearchInput from './SearchInput'
import { useRoutes } from '../../hooks/useRoutes'
import { TripDetails } from '../../context/TripContext'

export default function SearchPanel({ ref, onAirportSelect }) {

    // const [confirmed, setConfirmed] = useState(null)
    const [entries, setEntries] = useState([{ airport: null, error: null }])

    const { routes, fetchRoutes, clearRoutes } = useRoutes()

    const { addLeg, clearAll: clearTripAll } = useContext(TripDetails)

    async function handleConfirm(index, airport) {

        const updated = [...entries]
        if (index === 0) {
            onAirportSelect(airport)
            // setConfirmed(airport)
            updated[index] = { airport, error: null }
            setEntries(updated)
            await fetchRoutes(airport.id)
            return
        }

        // Destination row - validate against loaded routes
        const route = routes.find(
            r => r.from.id === entries[index - 1].airport?.id &&
                r.to.id === airport.id
        )

        if (!route) {
            updated[index] = { airport: null, error: 'No direct route available' }
            setEntries(updated)
            return
        }

        //Valid route — add leg
        // const from = entries[index - 1].airport
        updated[index] = { airport, error: null }
        setEntries(updated)
        addLeg(route)
        onAirportSelect(airport)
        await fetchRoutes(airport.id)

    }

    // Arrow clicked — add new empty row 
    function handleArrow() {
        setEntries(prev => [...prev, { airport: null, error: null }])
    }

    function handleClearAll(){
        setEntries([{ airport: null, error: null }])
        clearRoutes()
        clearTripAll()
    }

    useImperativeHandle(ref, () => {
        handleClearAll
    })

    return (
        <div className='search-panel'>
            {entries.map((entry, index) => (
                <div key={index}>
                    {/* Connector line between rows */}
                    {index > 0 && (
                        <div className='connector'>
                            <div className='connector-line'/>
                        </div>
                    )}
                    <SearchInput
                        confirmed={entry.airport}
                        onConfirm={(airport) => handleConfirm(index, airport)}
                        onArrow={handleArrow}
                        error={entry.error}
                    />
                </div>
            ))}
        </div>
    )
}
