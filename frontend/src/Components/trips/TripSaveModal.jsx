export default function TripSaveModal({ onClose }) {
  return (
    <div className="backdrop" style={{ zIndex: 3000, backdropFilter: 'blur(2px)' }} onClick={onClose}>
        <div className="trip-save-modal">
            <h2>For Saving Trip Legs</h2>
        </div>
    </div>
  )
}

