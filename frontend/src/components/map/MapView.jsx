import { useState, useCallback, useContext, useRef, useEffect } from 'react'
import Map from 'react-map-gl/maplibre';
// import { NavigationControl } from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

// import { DeckGL } from '@deck.gl/react'
import { ScatterplotLayer, ArcLayer, TextLayer } from '@deck.gl/layers'
import DeckGL from '@deck.gl/react'

import { useAirports } from '../../hooks/useAirports'
import { useRoutes } from '../../hooks/useRoutes'
import ContextMenu from './ContextMenu'
import { TripDetails } from '../../context/TripContext'
import { Theme } from '../../context/ThemeContext';

import SearchPanel from './SearchPanel' // added for search
import { FlyToInterpolator } from '@deck.gl/core';

import { TripsLayer } from '@deck.gl/geo-layers'
import { greatCircleMidpoint } from '../../services/greatCircle'


const INITIAL_VIEW = {
    longitude: 0,
    latitude: 20,
    zoom: 2,
    pitch: 0,
    bearing: 0,
}

const ANIMATION_SPEED = 0.3    // how fast the trail moves (lower = slower)
const TRAIL_LENGTH = 0.2    // length of fading trail (0-1)
const PULSE_SPEED = 0.05   // how fast available routes pulse

export default function MapView() {

    // To get all the required airports from backend
    const { airports, airportsLoading, addAirport } = useAirports()
    // Initail View state for Deck GL
    const [viewState, setViewState] = useState(INITIAL_VIEW)
    // To display airport details on hovering over dots
    const [hoveredAirport, setHoveredAirport] = useState(null)  // { id, name, city, country, x, y }
    // for airport click
    const [selectedAirport, setSelectedAirport] = useState(null)
    // To get the flight routes from backend
    const { routes, fetchRoutes, clearRoutes } = useRoutes()
    // For ContextMenu the right Click
    const [contextMenu, setContextMenu] = useState(null)  // { x, y }
    // For Route details on hover
    const [hoveredRoute, setHoveredRoute] = useState(null)  // { label, x, y }
    // For Route Selection - selectedRoute holds the current airports route which user selected
    // user is free to change it
    // history routes are the ones user already selected, it is for now will be fixed
    // const [ selectedRoute, setSelectedRoute] = useState([])
    // const [ historyRoute, setHistoryRoute] = useState([])
    // Since the display of a route can also be done by loading a trip from my trips we need 
    // populate the route details from a context - TripContext
    const { currentLeg: selectedRoute, addLeg, clearAll } = useContext(TripDetails)

    const searchPanelRef = useRef(null) // Added for search panel

    // Animation state
    const [animTime, setAnimTime] = useState(0)   // TripsLayer current time (0→1 loop)
    const [pulseTime, setPulseTime] = useState(0)   // pulse frame counter

    const animRef = useRef(null)

    // ── Airport click ──────────────────────────────────────────────
    const handleAirportClick = useCallback((airport) => {
        if (airport === selectedAirport) return
        flyto(airport)
        setSelectedAirport(airport)
        fetchRoutes(airport.id)
        // if (selectedRoute){
        //     // add leg
        //     setHistoryRoute(selectedRoute)
        // }       
    }, [selectedAirport, fetchRoutes]) //, selectedRoute])

    // ── Route click — select a specific flight path ────────────────
    const handleRouteClick = useCallback((route) => {
        if (!selectedAirport) return
        if (route === selectedRoute) return // Onclicking same route again do nothing for now
        // setSelectedRoute([...historyRoute, route]) // Old way without using context
        // //addLeg({ from: route.from, to: route.to, flightId: route.flightId }) // Commented as more details needed 
        // Find full airport details (has city) from airports list
        // const fromAirportDetails = airports.find(a => a.id === route.from.id) ?? route.from
        // const toAirportDetails   = airports.find(a => a.id === route.to.id)   ?? route.to
        // addLeg({
        //     from: { ...route.from, city: fromAirportDetails.city },
        //     to: { ...route.to,   city: toAirportDetails.city },
        //     flightId: route.flightId,
        // }) 
        // The above code no more needed as backend adjusted and useRoutes handles it.
        addLeg({ from: route.from, to: route.to, flightId: route.flightId })
        addAirport(route.to.id)

    }, [selectedAirport]) // ,historyRoute])    

    // Right click — show context menu
    function handleContextMenu(e) {
        e.preventDefault()
        setContextMenu({ x: e.clientX, y: e.clientY })
    }

    // Clear All
    const handleClearAll = useCallback(() => {
        clearRoutes()
        setSelectedAirport(null)
        // setSelectedRoute([])
        // setHistoryRoute([])
        clearAll()
        searchPanelRef.current?.handleClearAll()    // ← sync search panel
    }, [clearRoutes])

    // Single animation loop drives both effects
    useEffect(() => {
        let running = true

        const loop = () => {
            if (!running) return
            setAnimTime(t => (t + ANIMATION_SPEED * 0.01) % 1)
            setPulseTime(t => t + PULSE_SPEED)
            animRef.current = requestAnimationFrame(loop)
        }

        animRef.current = requestAnimationFrame(loop)
        return () => {
            running = false
            cancelAnimationFrame(animRef.current)
        }
    }, [])

    //Pulse width for available routes
    const pulseWidth = 1.5 + Math.sin(pulseTime) * 1.0
    // Trip -layer needs path + timestamps shape
    const tripPaths = selectedRoute.map(leg => ({
        path: [
            [leg.from.longitude, leg.from.latitude],
            [leg.to.longitude, leg.to.latitude],
        ],
        timestamps: [0, 1],
    }))

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
            // getWidth: 1.5,
            getWidth: pulseWidth,  // added for animation
            greatCircle: true,
            pickable: true,
            onHover: ({ object, x, y }) => {
                setHoveredRoute(object
                    ? { label: `${object.from.city} (${object.from.country}) → ${object.to.city} (${object.to.country})`,
                         x, y }
                    : null
                )
            },
            onClick: ({ object }) => object && handleRouteClick(object),
            updateTriggers: {
                getWidth: pulseWidth
            }
        }),

        // 2. Selected trip arc
        new ArcLayer({
            id: 'selected-route',
            data: selectedRoute,
            getSourcePosition: d => [d.from.longitude, d.from.latitude],
            getTargetPosition: d => [d.to.longitude, d.to.latitude],
            getSourceColor: [255, 140, 0, 220],
            getTargetColor: [255, 60, 60, 220],
            getWidth: 3,
            greatCircle: true,
            pickable: true,
            onHover: ({ object, x, y }) => {
                setHoveredRoute(object
                    ? { label: `${object.from.id} → ${object.to.id}`, x, y }
                    : null
                )
            },
        }),

        new TextLayer({
            id: 'selected-routes-labels',
            data: selectedRoute,
            getPosition: d => {
                const mid = greatCircleMidpoint(d.from, d.to)
                return [mid.longitude, mid.latitude]
            },
            getText: d => String(d.seq),
            getSize: 16,
            getColor: [255, 255, 255],
            getBackgroundColor: d => [255, 140, 0, 220],  // orange pill background
            background: true,
            backgroundPadding: [6, 3, 6, 3],              // [left, top, right, bottom]
            getBorderRadius: 8,
            getTextAnchor: 'middle',
            getAlignmentBaseline: 'center',
            fontWeight: 'bold',
            fontFamily: 'system-ui, sans-serif',
            billboard: true,                         // always faces camera
            pickable: false,
        }),

        //New Layer
        new TripsLayer({
            id: 'selected-routes-trail',
            data: tripPaths,
            getPath: d => d.path,
            getTimestamps: d => d.timestamps,
            getColor: [255, 220, 80],  // bright yellow trail
            widthMinPixels: 3,
            jointRounded: true,
            trailLength: TRAIL_LENGTH,
            // greatCircle: true,
            currentTime: animTime,   // ← drives animation
            updateTriggers: {
                currentTime: animTime
            },
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

    const { isDark } = useContext(Theme)

    const mapStyle = isDark
        ? 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json'
        : 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'

    // Added as part of search
    const flyto = useCallback((airport) => {
        setViewState(prev => ({
            ...prev,
            longitude: airport.longitude,
            latitude: airport.latitude,
            zoom: 6,
            transitionInterpolator: new FlyToInterpolator({ speed: 2 }),
            transitionDuration: 800,
        }))
    }, [])
    // End of Insert


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
                    if (isHovering) return 'pointer'
                    return 'grab'
                }}
            >
                <Map
                    mapStyle={mapStyle}
                />
                {/* </Map>     */}
            </DeckGL>

            {/* Search panel — top left, above map */}
            <SearchPanel
                ref={searchPanelRef}
                onAirportSelect={airport => {
                    //cannot call handleairport click as it might result in infinite loops
                    setSelectedAirport(airport)
                    flyto(airport)
                    fetchRoutes(airport.id)
                }}
            />

            {/* Airport tooltip */}
            {hoveredAirport && (
                <div
                    className='tooltip'
                    style={{ left: hoveredAirport.x + 12, top: hoveredAirport.y }}
                >
                    <strong>{hoveredAirport.id}</strong>
                    <span className='tooltip-sub'>{hoveredAirport.city}, {hoveredAirport.country}</span>
                </div>
            )}

            {/* Route tooltip */}
            {hoveredRoute && !hoveredAirport && (
                <div className='tooltip' style={{ left: hoveredRoute.x + 12, top: hoveredRoute.y + 15 }}>
                    <strong>{hoveredRoute.label}</strong>
                </div>
            )}

            {/* Right-click context menu */}
            {contextMenu && (
                <ContextMenu
                    x={contextMenu.x}
                    y={contextMenu.y}
                    onClearAll={handleClearAll}
                    onClose={() => setContextMenu(null)}
                />
            )}

            {/* Selected legs counter */}
            {selectedRoute.length > 0 && (
                <div className='legs-badge'>
                    {selectedRoute.length} leg{selectedRoute.length > 1 ? 's' : ''} selected
                </div>
            )}
        </div>
    )
}
