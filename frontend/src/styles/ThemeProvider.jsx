import { useEffect } from "react"

// Apply theme CSS variables to :root
function ThemeProvider({ theme, children }) {
  useEffect(() => {
    const root = document.documentElement
    Object.entries(theme).forEach(([key, val]) => root.style.setProperty(key, val))
  }, [theme])
  return children
}

export default ThemeProvider