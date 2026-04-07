import { createContext, useEffect } from "react"

const Theme = createContext(null)

// Apply theme CSS variables to :root
export default function ThemeContext({ theme, children }) {

  useEffect(() => {
    const root = document.documentElement
    Object.entries(theme).forEach(([key, val]) => root.style.setProperty(key, val))
  }, [theme])

  return (
    <Theme.Provider value={{}}>
      {children}
    </Theme.Provider>
  )
}
