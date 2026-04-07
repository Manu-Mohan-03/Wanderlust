
import { useContext, useEffect } from 'react'
import { useNavigate } from 'react-router'
import { TripDetails } from '../context/TripContext'
import { useTrips }        from '../hooks/useTrips'
import { AuthDetails } from '../context/AuthContext'

export default function TripsPage() {

    const navigate = useNavigate()
    const { loadTrip } = useContext(TripDetails)    
    const { trips, fetchTrips, toTripLegs, deleteTrip, loading, error } = useTrips()
    const { user } = useContext(AuthDetails)
    
    // Redirect if not logged in
    useEffect(() => {
        if (!user) navigate('/')
    }, [user])

    // Load trips on mount
    useEffect(() => {
        if (user) 
            fetchTrips(user.id)
    },[user])    

    function handleLoad(trip){
        const legs = toTripLegs(trip)
        loadTrip(legs)
        navigate('/')
    }

    async function handleDelete(e, tripId){
        e.stopPropagation()
        await deleteTrip(tripId)
    }

    return (
        <div className="page">    
            {/* Seperate Div to seperate background and content*/}
            <div className='trips-container'>      
                <div className="page-header">
                    <h1 className="title">My Trips</h1>
                    <button className="back-button" onClick={() => navigate('/')}>
                        ← Back to Map
                    </button>
                </div>

                {loading && (
                    <div className='info-message'>Loading your trips...</div>
                )}
                {error && (
                    <div className='error-message'>{error}</div>
                )}    

                {!loading && !error && trips.length === 0 && (
                <div className='empty-state'>
                    <div className='empty-icon'>🗺️</div>
                    <p className='empty-text'>No saved trips yet</p>
                    <button className='goto-map-button' onClick={() => navigate('/')}>
                        Start Planning
                    </button>
                </div>
                )}                

                <div className="grid">
                    {trips.map(trip => (
                        <div key = {trip.trip_id} className="card">
                            {/* Card header */}
                            <div className="card-header">
                                <span className="trip-name">
                                    {trip.name}
                                </span>
                            </div>
                            {/* Legs list */}
                            <div className="legs-list">
                                {trip.trip_details.map(leg => (
                                    <div key={leg.leg_no} className="leg-row">
                                        <span className="leg-seq">{leg.leg_no}</span>
                                        <span className="leg-route">
                                            {leg.origin_city}
                                            {' → '}
                                            {leg.destination_city}                                        
                                        </span>
                                        <span className="leg-flight">
                                            {leg.flight_details.flight_id}
                                        </span>
                                    </div>
                                ))}
                            </div>
                            {/* User Actions */}
                            <div className="card-actions">
                                <button className="load-button" onClick={()=>handleLoad(trip)}>
                                    🗺️ Load on Map        
                                </button> 
                                <button className="delete-button" onClick={(e) => handleDelete(e, trip.trip_id)}>
                                    🗑️        
                                </button>       
                            </div>
                        </div>
                    ))}
                </div>
            </div>  
        </div>
    )
}
