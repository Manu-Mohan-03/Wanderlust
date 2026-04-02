
import { createContext } from "react"

const TripDetails = createContext(null)

export default function TripContext({children}) {
  return (
    <TripDetails.Provider>
        {children}
    </TripDetails.Provider>
  )
}

