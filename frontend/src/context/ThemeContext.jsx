import { useEffect } from "react"


// Apply theme CSS variables to :root
export default function ThemeContext({ theme, children }) {
  useEffect(() => {
    const root = document.documentElement
    Object.entries(theme).forEach(([key, val]) => root.style.setProperty(key, val))
  }, [theme])
  return children
}
