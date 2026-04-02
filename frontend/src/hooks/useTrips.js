export function toTripLegs(trip){
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