import React, { useRef, useEffect } from 'react'
import { useAirportSearch } from '../../hooks/useAirportSearch'

export default function SearchInput({ confirmed, onConfirm, onArrow, error }) {

    const { searchQuery, setSearchQuery, results, loading, clear } = useAirportSearch()
    const inputRef = useRef(null)

    // Temp for testing, since we need make the airport selected, it cant live here
    // const [confirmed, setConfirmed] = useState(null) 

    function handleSelect(airport) {
        clear()
        // setConfirmed({
        //     id: airport.id,
        //     name: airport.name
        // })
        onConfirm(airport)
    }

    // Auto focus new empty rows
    useEffect(() => {
        if (!confirmed) inputRef.current?.focus()
    }, [confirmed])

    if (confirmed) {
        return (
            <div className='search-row'>
                <div className='confirmed-box' style={{ borderColor: error ? '#fecaca' : 'var(--border)' }}>
                    <span className='confirmed-icon'>✈</span>
                    <div className='confirmed-text'>
                        <span className='confirmed-code'>{confirmed.id}</span>
                        <span className='confirmed-name'>{confirmed.name}</span>
                    </div>
                    {/* {error && (
                        <span className='error-text'>{error}</span>
                    )} */}
                </div>
                {!error && (
                    <button
                        className='arrow-button'
                        title="Select destination airport"
                        onClick={onArrow}
                    >
                        →
                    </button>
                )}
            </div>
        )
    }

    return (
        <div className='search-row'>
            <div className='input-wrapper'>
                <span className='search-icon' >🔍</span>
                <input
                    ref={inputRef}
                    className='search-input'
                    type="text"
                    placeholder="Enter Airport/City"
                    value={searchQuery}
                    onChange={e => setSearchQuery(e.target.value)}
                />

                {/* DropDown here*/}
                {results.length > 0 && (
                    <div className='result-dropdown'>
                        {results.map(airport => (
                            <button
                                key={airport.id}
                                className='result-item'
                                onClick={() => handleSelect(airport)}
                            >
                                <span className='result-main' >{airport.id}</span>
                                <span className='result-info' >
                                    {airport.city}, {airport.country}
                                </span>
                            </button>
                        ))}
                    </div>
                )}

                {/* No results */}
                {searchQuery.length >= 2 && !loading && results.length === 0 && (
                    <div className='result-dropdown'>
                        <div className='no-results'>                            
                            No airports found
                        </div>
                    </div>                  
                )}
                {/* No Direct Routes */}  
                {error && (
                    <div className='result-dropdown'>
                        <div className='no-results'>                            
                            {error}
                        </div>
                    </div>
                )}
            </div>
        </div>


    )
}
