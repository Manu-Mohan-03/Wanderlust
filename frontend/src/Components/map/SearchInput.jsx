import React from 'react'

export default function SearchInput() {
 return (
    <div className='search-row'>
      <div className='input-wrapper'>
        <span className='search-icon' >🔍</span>
        <input
          className='search-input' 
          type="text"
          placeholder="Enter Airport/City"
        />
      </div>
    </div>
  )
}

