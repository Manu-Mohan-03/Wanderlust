import MapPage from "./pages/MapPage"
import { lightTheme } from './styles/theme'
import ThemeProvider from "./styles/ThemeProvider"

import Header from './components/layout/Header'

export default function App() {
  return (
    <ThemeProvider theme={lightTheme}>
      <Header/>
      <MapPage />
    </ThemeProvider>
  )
}
