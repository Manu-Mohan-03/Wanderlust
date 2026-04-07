import { useContext, useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router'

import AuthModal from '../auth/AuthModal'
import { AuthDetails } from '../../context/AuthContext'
import TripSaveModal from '../trips/TripSaveModal'
import { useTrips } from '../../hooks/useTrips'
import { TripDetails } from '../../context/TripContext'


export default function Header() {
    // To display dialog box for signing in
    const [showAuthModal, setShowAuthModal] = useState(false)
    // Toggle Menu for user details
    const [menuOpen, setMenuOpen] = useState(false)
    // To display dialog box for saving
    const [showSaveModal, setShowSaveModal] = useState(false)
    // For Authentication 
    const { user, logout } = useContext(AuthDetails)
    // For navigating to different Pages
    const navigate = useNavigate()
    // For usermenu handling : clicking outside the menu 
    const menuRef = useRef(null)
    // For Saving the trips
    const { saveTrip, loading: saving, error } = useTrips()
    // To get the trip legs selected
    const { currentLeg: selectedLegs } = useContext(TripDetails)
    // For notifing save success
    const [saveSuccess,   setSaveSuccess] = useState(false)
    const [showSaveStatus, setShowSaveStatus] = useState('')


    function goTo(path) {
        setMenuOpen(false)
        navigate(path)
    }

    function handleLogout() {
        logout()
        setMenuOpen(false)
        navigate('/')
    }
    function handleSaveClick() {
        setMenuOpen(false)
        setShowSaveModal(true)
    }

    // Close dropdown if user clicks outside
    useEffect(() => {
        function handleClickOutside(e) {
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setMenuOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])
    // For Saving the Trip Legs along with the trip-name (optional) from the Modal
    async function handleConfirmSave(tripName) {
        setShowSaveStatus(true)
        try {
            const newTrip = await saveTrip(selectedLegs, user.id, tripName)
            setShowSaveModal(false)
            setSaveSuccess(true)
            setTimeout(() => {
                setShowSaveStatus(false)
                setSaveSuccess(false)
            }, 3000)
        } catch(err) {
            setTimeout(() => {
                setShowSaveStatus(false)
            },3000)
        }
    }

    function disableSave(){
        if (saving) return true
        return selectedLegs.length > 0 ? false : true
    }

    return (
        <>
            <header className='header'>

                {/* Left — Logo */}
                <div className='logo' onClick={() => navigate('/')}>
                    ✈️ <span className='logo-text'>WanderLust</span>
                </div>

                {/* Right — Login Button*/}
                <div className='right'>
                    {user ? (
                        // <> 
                        //     <span className='user-email'>{user.email}</span>
                        //     <button className="btn" onClick={logout}>
                        //         Sign Out
                        //     </button>                        
                        // </>
                        <div className='usermenu' ref={menuRef}>
                            <button
                                className='icon-button'
                                onClick={() => setMenuOpen(prev => !prev)}
                                title={user.email}
                            >
                                👤
                            </button>

                            {menuOpen && (
                                <div className='dropdown'>
                                    <div className='dropdown-header'>
                                        <span className='dropdown-email'>{user.email}</span>
                                    </div>
                                    <hr className='divider' />
                                    <button className='dropdown-item' onClick={() => goTo('/account')}>
                                        👤 My Account
                                    </button>
                                    <button className='dropdown-item' onClick={() => goTo('/trips')}>
                                        🗺️ My Trips
                                    </button>
                                    <hr className='divider' />
                                    <button
                                        className='dropdown-item'
                                        onClick={handleSaveClick}
                                        disabled={disableSave}
                                    >
                                        💾 Save Trip
                                    </button>
                                    <hr className='divider' />
                                    <button
                                        className='dropdown-item signout-item'
                                        onClick={handleLogout}
                                    >
                                        🚪 Sign Out
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <button className="login-button" onClick={() => setShowAuthModal(true)}>
                            Sign In
                        </button>
                    )}
                </div>
            </header>

            {/* Login/SignUp modal —onClose prop to close the modal on clicking any where on the overlay */}
            {showAuthModal && <AuthModal onClose={() => setShowAuthModal(false)} />}
            {/*To Save the trips Selected*/}
            {showSaveModal && <TripSaveModal
                onClose={() => setShowSaveModal(false)}
                onSave={handleConfirmSave}
                loading={saving}
            />
            }
            {showSaveStatus && (
                <div 
                    className='save-status'
                    style={{ background: saveSuccess ?  '#22c55e' : error ? '#ef4444' : saving && '#f59e0b'}}
                >
                    {/* Success / Error / Saving */}
                    { saveSuccess ? '✓ Trip Saved!' : saving ? "Saving..." : error }
                </div>
            )}

        </>
    )
}
