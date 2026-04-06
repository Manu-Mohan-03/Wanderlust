import { useState } from "react"
import { tripAPI } from "../services/api"


// Map TripContext legs → TripIn shape backend expects
function toTripIn(legs, userId, tripName) {
  return {
    user_id: userId,
    name: tripName ?? null,
    trip_legs: legs.map(leg => ({
      leg_no: leg.seq,
      mode: 'flight',
      origin_city: leg.from.city ?? leg.from.id,
      destination_city: leg.to.city ?? leg.to.id,
      leg_start: null,
      leg_stop: null,
      flight: {
        flight_id: leg.flightId,
      },
    })),
  }
}

// Map TripOut → TripContext legs shape (for loading onto map)
function toTripLegs(tripOut) {
  return tripOut.trip_details.map(leg => ({
    seq: leg.leg_no,
    flightId: leg.flight_details?.flight_id ?? null,
    from: {
      id: leg.flight_details?.flight_data?.orig_airport,
      name: leg.flight_details?.flight_data?.orig_airport_details?.name,
      city: leg.origin_city,
      latitude: leg.flight_details?.flight_data?.orig_airport_details?.latitude,
      longitude: leg.flight_details?.flight_data?.orig_airport_details?.longitude,
    },
    to: {
      id: leg.flight_details?.flight_data?.dest_airport,
      name: leg.flight_details?.flight_data?.dest_airport_details?.name,
      city: leg.destination_city,
      latitude: leg.flight_details?.flight_data?.dest_airport_details?.latitude,
      longitude: leg.flight_details?.flight_data?.dest_airport_details?.longitude,
    },
  }))
}

export function useTrips() {

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [trips, setTrips] = useState([])

  async function saveTrip(legs, userId, tripName) {
    setLoading(true)
    setError(null)
    try {
      console.log("Confirm useTrips")
      const requestBody = toTripIn(legs, userId, tripName)
      
      const saved = await tripAPI.save(requestBody)
      // setTrips(prev => [saved])
      return saved
    } catch (err) {
      setError('Failed to save trip')
      console.error(err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  async function fetchTrips(userId) {
    setLoading(true)
    setError(null)    
    try {
      const data = await tripAPI.getAll(userId) 
      setTrips(data)
    } catch (err) {
      setError('Failed to load trip')
      console.error(err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  async function deleteTrip(tripId) {
    try {
      await tripAPI.delete(tripId)
      setTrips(prev => prev.filter(trip => 
        trip.trip_id !== tripId ))
    } catch (err) {
        console.error(err)
    } 
  }

  return {
    trips,
    saveTrip,
    fetchTrips,
    toTripLegs,  // exported so TripsPage can use it
    deleteTrip,
    loading
  }

}