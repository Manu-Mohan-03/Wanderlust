
import { useContext } from 'react'
import { useNavigate } from 'react-router'
import { TripDetails } from '../context/TripContext'
import { toTripLegs }        from '../hooks/useTrips'


// Temporary Test Data for building and Unit Testing of Trips Page
const TRIPS = [{
  user_id: 7,
  trip_id: 1,
  name: "My Euro Trip",        
  trip_legs: [
    {
      leg_no: 1,               
      mode: "flight",          
      origin_city: "Frankfurt", 
      destination_city: "Phoenix",
      leg_start: null,         
      leg_stop:  null,         
      flight: {
        flight_id: "DE2026"    
      }
    }
  ]
}]

export default function TripsPage() {

    const navigate = useNavigate()
    const { loadTrip } = useContext(TripDetails)

    function handleLoad(trip){
        const legs = toTripLegs(trip)
        loadTrip(legs)
        navigate('/')
    }
    function handleDelete(trip){
        // To be implemented
    }

    return (
        <div className="trips-page">    
            {/* Seperate Div to seperate background and content*/}
            <div className='container'>      
                <div className="page-header">
                    <h1 className="title">My Trips</h1>
                    <button className="back-button" onClick={() => navigate('/')}>
                        ← Back to Map
                    </button>
                </div>
                <div className="grid">
                    {TRIPS.map(trip => (
                        <div key = {trip.trip_id} className="card">
                            {/* Card header */}
                            <div className="card-header">
                                <span className="trip-name">
                                    {trip.name}
                                </span>
                            </div>
                            {/* Legs list */}
                            <div className="legs-list">
                                {trip.trip_legs.map(leg => (
                                    <div key={leg.leg_no} className="leg-row">
                                        <span className="leg-seq">{leg.leg_no}</span>
                                        <span className="leg-route">
                                            {leg.origin_city}
                                            {' → '}
                                            {leg.destination_city}                                        
                                        </span>
                                        <span className="leg-flight">
                                            {leg.flight.flight_id}
                                        </span>
                                    </div>
                                ))}
                            </div>
                            {/* User Actions */}
                            <div className="card-actions">
                                <button className="load-button" onClick={()=>handleLoad(trip)}>
                                    🗺️ Load on Map        
                                </button> 
                                <button className="delete-button" onClick={() => handleDelete(trip)}>
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
