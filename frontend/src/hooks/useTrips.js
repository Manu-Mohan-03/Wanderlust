import { useState } from "react"
import { tripAPI } from "../services/api"

export function sampleLegs(trip) {
  // Test data
  return [
    {
      from: {
        id: "FRA",
        name: "Frankfurt Airport",
        city: "Frankfurt",
        latitude: 50.0379,
        longitude: 8.5622
      },
      to: {
        id: "ORD",
        name: "Chicago O'Hare International Airport",
        city: "Chicago",
        latitude: 41.9742,
        longitude: -87.9073
      },
      flightId: "LH430",
      seq: 1
    },
    {
      from: {
        id: "ORD",
        name: "Chicago O'Hare International Airport",
        city: "Chicago",
        latitude: 41.9742,
        longitude: -87.9073
      },
      to: {
        id: "PHX",
        name: "Phoenix Sky Harbor International Airport",
        city: "Phoenix",
        latitude: 33.4342,
        longitude: -112.0116
      },
      flightId: "UA1885",
      seq: 2
    }
  ]
}

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
    // setLoading(true)
    // setError(null)
    try {
      console.log("Confirm useTrips")
      const requestBody = toTripIn(legs, userId, tripName)
      
      const saved = await tripAPI.save(requestBody)
      // setTrips(prev => [saved])
      return saved
    } catch (err) {
      // setError('Failed to save trip')
      console.error(err)
      throw err
    } finally {
      // setLoading(false)
    }
  }

  async function fetchTrips(user) {
    // setLoading(true)
    // setError(null)    
    try {
      // const data = await tripAPI.getAll() // since data already available in user
      const data = user?.user_trips ?? []
      console.log("Trip legs: ", data)
      setTrips(data)
    } catch (err) {
      // setError('Failed to load trip')
      console.error(err)
      throw err
    } finally {
      // setLoading(false)
    }
  }

  return {
    trips,
    saveTrip,
    fetchTrips,
    toTripLegs
  }

}