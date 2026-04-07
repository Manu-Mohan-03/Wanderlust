import MapPage from "./pages/MapPage"
import { lightTheme } from './styles/theme'
import ThemeContext from "./context/ThemeContext"
import Header from './components/layout/Header'
import AuthContext from "./context/AuthContext"
import TripContext from "./context/TripContext"

import { BrowserRouter, Routes, Route } from 'react-router'
import AccountPage from "./pages/AccountPage"
import TripsPage from "./pages/TripsPage"

export default function App() {
  return (
    <ThemeContext theme={lightTheme}>
      <AuthContext>
        <TripContext>
          <BrowserRouter>
            <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
              <Header/>
              <main style={{ 
                flex: 1, 
                overflowX: 'hidden', 
                overflowY: 'auto'
              }}> 
                <Routes>
                  <Route path='/' element={<MapPage />}/>
                  <Route path='/account' element={<AccountPage/>}/>
                  <Route path='/trips' element={<TripsPage />}/>
                </Routes>             
              </main>
            </div>
          </BrowserRouter>
        </TripContext>
      </AuthContext>
    </ThemeContext>
  )
}
