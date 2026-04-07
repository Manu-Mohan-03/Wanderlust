// To apply theme CSS variables to :root
import { createContext, useEffect, useState } from "react"
import { lightTheme, darkTheme } from "../styles/theme"

const Theme = createContext(null)

export default function ThemeContext({ children }) {

  // const [ theme, setTheme ] = useState(lightTheme)
  const [isDark, setIsDark] = useState(false)

  // Apply CSS variables to :root whenever theme changes
  useEffect(() => {
    const theme = isDark ? darkTheme : lightTheme
    const root = document.documentElement
    Object.entries(theme).forEach(([key, val]) => root.style.setProperty(key, val))
  }, [isDark])

  function toggleTheme() {
    // setMode(prev => (
    //   prev === lightTheme ? darkTheme : lightTheme
    // ))
    setIsDark(prev => !prev)
  }

  return (
    <Theme.Provider value={{ toggleTheme, isDark }}>
      {children}
    </Theme.Provider>
  )
}

export { Theme }
