import React from 'react'
import Map from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css'; 

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'

function MapView() {
  return (
    <div
      style={{ width: '100%', height: '100vh', position: 'relative' }}>
        <Map mapStyle={MAP_STYLE} />
    </div>
  )
}

export default MapView