import MapPage from "./pages/MapPage"
import { lightTheme } from './styles/theme'
import ThemeProvider from "./styles/ThemeProvider"
import Header from './components/layout/Header'
import AuthContext from "./context/AuthContext"

export default function App() {
  return (
    <ThemeProvider theme={lightTheme}>
      <AuthContext>
        <Header/>
        <MapPage />
      </AuthContext>
    </ThemeProvider>
  )
}
