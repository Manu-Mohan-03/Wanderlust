import { useState, useCallback } from 'react'
import Map from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

// import { DeckGL } from '@deck.gl/react'
import { ScatterplotLayer, ArcLayer } from '@deck.gl/layers'
import DeckGL from '@deck.gl/react'

import { useAirports } from '../../hooks/useAirports'
import { useRoutes } from '../../hooks/useRoutes'
import ContextMenu from './ContextMenu';

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'

const INITIAL_VIEW = {
    longitude: 0,
    latitude: 20,
    zoom: 2,
    pitch: 0,
    bearing: 0,
}

export default function MapView() {

    // To get all the required airports from backend
    const { airports, airportsLoading } = useAirports()
    // Initail View state for Deck GL
    const [viewState, setViewState] = useState(INITIAL_VIEW)
    // To display airport details on hovering over dots
    const [hoveredAirport, setHoveredAirport] = useState(null)  // { id, name, city, country, x, y }
    // for airport click
    const [selectedAirport, setSelectedAirport] = useState(null)  
    // for flight routes
    const { routes, fetchRoutes } = useRoutes()
    // For ContextMenu the right Click
    const [contextMenu, setContextMenu] = useState(null)  // { x, y }

    // ── Airport click ──────────────────────────────────────────────
    const handleAirportClick = useCallback((airport) => {
        setSelectedAirport(airport)
        fetchRoutes(airport.id)        
    }, [selectedAirport, fetchRoutes])

    function handleContextMenu(e){
        e.preventDefault()
        setContextMenu({ x: e.clientX, y: e.clientY })
    }

    // ── Deck.gl layers ────────────────────────────────────────────   
    const layers = [

        // 1. Available routes (from selected airport)
        new ArcLayer({
            id: 'available-routes',
            data: routes,
            getSourcePosition: d => [d.from.longitude, d.from.latitude],
            getTargetPosition: d => [d.to.longitude, d.to.latitude],
            getSourceColor: [100, 160, 255, 120],
            getTargetColor: [100, 160, 255, 120],
            getWidth: 1.5,
            greatCircle: true,
        }),

        // Airport markers
        new ScatterplotLayer({
            id: 'airports',
            data: airports,
            getPosition: d => [d.longitude, d.latitude], // d is each airport from airports
            getRadius: 6000, // one cover 6 km radius on actual earth
            radiusMinPixels: 3, // 
            radiusMaxPixels: 10,
            getFillColor: d => d.id === selectedAirport?.id
                ? [255, 140, 0]   // selected — orange
                : [30, 100, 255], // default — blue
            pickable: true,
            onHover: ({ object, x, y }) => {
                setHoveredAirport(object ? { ...object, x, y } : null)
            },
            onClick: ({ object }) => object && handleAirportClick(object),
            updateTriggers: {
                getFillColor: [selectedAirport?.id]
            },            
        })
    ]

    return (
        <div
            className='map-view'
            onContextMenu={handleContextMenu}
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
                getCursor={({ isHovering, isDragging }) => {
                    if (isHovering)   return 'pointer'
                    return 'grab'
                }}                
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

            {/* Right-click context menu */}
            {contextMenu && (
                <ContextMenu
                    x={contextMenu.x}
                    y={contextMenu.y}
                />
            )}
        </div>
    )
}
