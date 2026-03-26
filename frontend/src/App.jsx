import MapPage from "./pages/MapPage"
import { lightTheme } from './styles/theme'
import ThemeProvider from "./styles/ThemeProvider"


export default function App() {
  return (
    <ThemeProvider theme={lightTheme}>
      <h1>Welcome to Wanderlust</h1>
      <MapPage />
    </ThemeProvider>
  )
}
