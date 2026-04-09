

import greatCircle from '@turf/great-circle'
import { point } from '@turf/helpers'

/**
 * Generates points along a great circle arc using Turf.js
 * Returns array of [longitude, latitude] pairs for TripsLayer / TextLayer
 */
export function interpolateGreatCircle(from, to, numPoints = 100) {
    try {
        const start = point([from.longitude, from.latitude])
        const end = point([to.longitude, to.latitude])

        const arc = greatCircle(start, end, { npoints: numPoints })

        // Turf returns a GeoJSON LineString or MultiLineString
        const coords = arc.geometry.type === 'LineString'
            ? arc.geometry.coordinates
            : arc.geometry.coordinates[0]   // MultiLineString — take first segment

        return coords   // already [[lon, lat], [lon, lat], ...]
    } catch (err) {
        // Fallback for edge cases (same point, antipodal points)
        console.warn('greatCircle fallback:', err)
        return [
            [from.longitude, from.latitude],
            [to.longitude, to.latitude],
        ]
    }
}

/**
 * Returns the geographic midpoint of a great circle arc
 */
export function greatCircleMidpoint(from, to, numPoints = 100) {
    const points = interpolateGreatCircle(from, to, numPoints)
    const mid = points[Math.floor(points.length / 2)]
    return { longitude: mid[0], latitude: mid[1] }
}

/**
 * Generates evenly spaced timestamps (0 → 1) for each point
 */
export function generateTimestamps(coords) {
  return coords.map((_, i) => i / (coords.length - 1))
}