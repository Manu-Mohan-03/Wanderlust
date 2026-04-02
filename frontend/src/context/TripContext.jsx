
import { createContext, useState } from "react"

const TripDetails = createContext(null)

export default function TripContext({children}) {
    // For the currently selected route
    const [ currentLeg, setCurrentLeg ] = useState([])

    // For previously selected Legs
    const [historyLegs, setHistoryLegs ] = useState([]) 

    //Helper function to add a leg
    function addLeg(leg){
        // Save the current leg to history before adding new leg
        setHistoryLegs([...historyLegs, currentLeg])
        // Create the new leg with a sequence number
        const newLeg = { ...leg, seq: currentLeg.length + 1 }
        // Update the active list
        setCurrentLeg([...currentLeg, newLeg])
    }

    // Helper to clear everything
    function clearAll(){
        setHistoryLegs([])
        setCurrentLeg([])
    }

    // To load the trip from a user profile
    function loadTrip(legs){
        setHistoryLegs([])
        setCurrentLeg(legs)
    } 

    return (
        <TripDetails.Provider value={{ currentLeg, addLeg, clearAll, loadTrip}}>
            {children}
        </TripDetails.Provider>
    )
}

export { TripDetails }
