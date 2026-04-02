import { useState } from "react"

export default function TripSaveModal({ onClose, onSave }) {

    const [ name, setName ] = useState('')

    function handleSave(){
        onSave(name || null)  // null = unnamed trip, backend accepts it
    }

    return (
        <div className="backdrop" style={{ zIndex: 3000, backdropFilter: 'blur(2px)' }}>
            <div className="trip-save-modal">
                <button className='close-button' onClick={onClose}>✕</button>
                <h2 className='title'>Save Trip</h2>
                <p className='sub-title'>Give your trip a name (optional)</p>
                <input
                    className='input'
                    type="text"
                    placeholder="e.g. Euro Summer 2026"
                    value={name}
                    onChange={e => setName(e.target.value)}
                />  
                <div className='actions'>
                    <button className='cancel-button' onClick={onClose}>
                        Cancel
                    </button>
                    <button
                        className="save-button"
                        onClick={handleSave}
                    >
                        💾 Save Trip
                    </button>
                </div>                      
            </div>
        </div>
    )
}

