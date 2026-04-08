// Handles all the logic of integrating with MapView and SearchInput
import { useState } from 'react'
import SearchInput from './SearchInput'

export default function SearchPanel({ onAirportSelect }) {

  const [confirmed, setConfirmed] = useState(null)   

  function handleConfirm(airport){
    onAirportSelect(airport)
    setConfirmed(airport)
  }  

  return (
    <SearchInput 
        confirmed={confirmed}
        onConfirm={(airport) => handleConfirm(airport)}
    />
  )
}

