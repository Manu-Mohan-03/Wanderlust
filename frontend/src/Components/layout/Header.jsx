import { useContext, useState } from 'react'
import AuthModal    from '../auth/AuthModal'
import { AuthDetails } from '../../context/AuthContext'

export default function Header() {

    const [showModal, setShowModal] = useState(false)
    const { user, logout } = useContext(AuthDetails)

    return (
       <>
            <header className='header'>

                {/* Left — Logo */}
                <div className='logo'>
                ✈️ <span className='logo-text'>WanderLust</span>
                </div>

                {/* Right — Login Button*/}
                <div className='right'>
                    {user ? (
                        <button className="btn" onClick={logout}>
                            Sign Out
                        </button>                        
                    ) : (
                        <button className="btn" onClick={() => setShowModal(true)}>
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
