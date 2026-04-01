import MapPage from "./pages/MapPage"
import { lightTheme } from './styles/theme'
import ThemeProvider from "./styles/ThemeProvider"
import Header from './components/layout/Header'
import AuthContext from "./context/AuthContext"

import { BrowserRouter, Routes, Route } from 'react-router'

export default function App() {
  return (
    <ThemeProvider theme={lightTheme}>
      <AuthContext>
        <BrowserRouter>
          <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
            <Header/>
            <main style={{ flex: 1, overflow: 'hidden' }}> 
              <Routes>
                <Route path='/' element={<MapPage />}/>
              </Routes>             
            </main>
          </div>
        </BrowserRouter>
      </AuthContext>
    </ThemeProvider>
  )
}
