import { useState } from 'react'
import AuthModal    from '../auth/AuthModal'

export default function Header() {

    const [showModal, setShowModal] = useState(false)

    return (
       <>
            <header className='header'>
                {/* Left — Logo */}
                <div className='logo'>
                ✈️ <span className='logo-text'>WanderLust</span>
                </div>
                {/* Right — Login Button*/}
                <div className='right'>
                    <button className="btn" onClick={() => setShowModal(true)}>
                        Sign In
                    </button>
                </div>
            </header>
            {/* Login/SignUp modal — only mounts when needed */}
            {showModal && <AuthModal />}
       </>
    )
}
