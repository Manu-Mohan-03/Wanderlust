import { useState } from 'react'
import Map from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

// import { DeckGL } from '@deck.gl/react'
import { ScatterplotLayer } from '@deck.gl/layers'
import DeckGL from '@deck.gl/react'

import { useAirports } from '../../hooks/useAirports'


const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'

const INITIAL_VIEW = {
    longitude: 0,
    latitude: 20,
    zoom: 2,
    pitch: 0,
    bearing: 0,
}

function MapView() {
    // To get all the required airports from backend
    const { airports, airportsLoading } = useAirports()
    // Initail View state for Deck GL
    const [viewState, setViewState] = useState(INITIAL_VIEW)


    // ── Deck.gl layers ────────────────────────────────────────────   
    const layers = [
        // Airport markers
        new ScatterplotLayer({
            id: 'airports',
            data: airports,
            getPosition: d => [d.longitude, d.latitude], // d is each airport from airports
            getRadius: 6000, // one cover 6 km radius on actual earth
            radiusMinPixels: 4, // 
            radiusMaxPixels: 10,
        })
    ]

    return (
        <div
            className='map-view'
        >
            {/* Loading indicator */}
            {airportsLoading && (
                <div className="loading-badge">Loading airports...</div>
            )}
            <DeckGL
                viewState={viewState}
                onViewStateChange={({ viewState }) => setViewState(viewState)}
                controller={true}
                layers={layers}
                style={{ position: 'absolute', inset: 0 }}
            >
                <Map mapStyle={MAP_STYLE} />
            </DeckGL>

        </div>
    )
}

export default MapView