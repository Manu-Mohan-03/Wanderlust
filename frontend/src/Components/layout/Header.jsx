import { useContext, useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router'

import AuthModal    from '../auth/AuthModal'
import { AuthDetails } from '../../context/AuthContext'


export default function Header() {
    // To display dialog box for signing in
    const [showModal, setShowModal] = useState(false)
    // Toggle Menu for user details
    const [ menuOpen, setMenuOpen ] = useState(false)
    const { user, logout } = useContext(AuthDetails)    
    const navigate = useNavigate()
    const menuRef = useRef(null)

    function goTo(path){
        setMenuOpen(false)
        navigate(path)
    }

    function handleLogout(){
        logout()
        setMenuOpen(false)
        navigate('/')
    }

    // Close dropdown if user clicks outside
    useEffect(() => {
        function handleClickOutside(e){
            if (menuRef.current && !menuRef.current.contains(e.target)) {
                setMenuOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    },[])

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
                                        className='dropdown-item signout-item'
                                        onClick={handleLogout}
                                    >
                                        🚪 Sign Out
                                    </button>
                                </div>
                            )}

                        </div>
                    ) : (
                        <button className="login-button" onClick={() => setShowModal(true)}>
                            Sign In
                        </button>
                    )}                  
                </div>
            </header>

            {/* Login/SignUp modal — only mounts when needed, onClose prop to close the modal on clicking 
                any where on the overlay */}
            {showModal && <AuthModal onClose={() => setShowModal(false)}/>}
       </>
    )
}
