import React, { useState } from 'react'
import { useAirportSearch } from '../../hooks/useAirportSearch'

export default function SearchInput({ confirmed , onConfirm }) {

    const { searchQuery, setSearchQuery, results, loading, clear } = useAirportSearch()

    // Temp for testing, since we need make the airport selected, it cant live here
    // const [confirmed, setConfirmed] = useState(null) 

    function handleSelect(airport) {
        console.log("Clicked Airport")
        clear()
        // setConfirmed({
        //     id: airport.id,
        //     name: airport.name
        // })
        onConfirm(airport)
    }

    if (confirmed) {
        return (
            <div className='search-row'>
                <div className='confirmed-box'>
                    <span className='confirmed-icon'>✈</span>
                    <div className='confirmed-text'>
                        <span className='confirmed-code'>{confirmed.id}</span>
                        <span className='confirmed-name'>{confirmed.name}</span>
                    </div>
                </div>
                <button className='arrow-button' title="Add next leg">
                    →
                </button>
            </div>
        )
    }

    return (
        <div className='search-row'>
            <div className='input-wrapper'>
                <span className='search-icon' >🔍</span>
                <input
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

            </div>
        </div>


    )
}
