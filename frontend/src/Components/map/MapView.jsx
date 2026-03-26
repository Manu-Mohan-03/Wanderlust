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
    // To display airport details on hovering over dots
    const [hoveredAirport, setHoveredAirport] = useState(null)  // { id, name, city, country, x, y }


    // ── Deck.gl layers ────────────────────────────────────────────   
    const layers = [
        // Airport markers
        new ScatterplotLayer({
            id: 'airports',
            data: airports,
            getPosition: d => [d.longitude, d.latitude], // d is each airport from airports
            getRadius: 6000, // one cover 6 km radius on actual earth
            radiusMinPixels: 3, // 
            radiusMaxPixels: 10,
            getFillColor: [30, 100, 255],
            pickable: true,
            onHover: ({ object, x, y }) => {
                setHoveredAirport(object ? { ...object, x, y } : null)
            }
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

            {/* Airport tooltip */}
            {hoveredAirport && (
                <div 
                    className='tooltip'
                    style={{ left: hoveredAirport.x + 12, top: (hoveredAirport.y - 10) + 130 }} // 130 px is the size of header
                >
                    <strong>{hoveredAirport.id}</strong>
                    <span className='tooltip-sub'>{hoveredAirport.city}, {hoveredAirport.country}</span>
                </div>
            )}
        </div>
    )
}

export default MapView