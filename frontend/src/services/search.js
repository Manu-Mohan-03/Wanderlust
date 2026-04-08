
export function filterAirports(
    airports,
    query
) {
    if (!query.trim()) return airports;

    const q = query.toLowerCase().trim();

    const results = airports.filter((airport) => {
        const airportCode = airport.airport_key?.toLowerCase() || "";
        const airportName = airport.name?.toLowerCase() || "";
        const cityName = airport.city?.name?.toLowerCase() || "";
        const countryName = airport.city?.country?.name?.toLowerCase() || "";
        const countryCode = airport.city?.country_key?.toLowerCase() || "";

        return (
            airportCode.includes(q) || airportName.includes(q) ||
            cityName.includes(q) || countryName.includes(q) || countryCode.includes(q)
        )
    })
    return results
}