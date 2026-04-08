import React from 'react'
import { useAirportSearch } from '../../hooks/useAirportSearch'

export default function SearchInput() {

    const { searchQuery, setSearchQuery, results, loading } = useAirportSearch()

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
 
            </div>
        </div>


    )
}

