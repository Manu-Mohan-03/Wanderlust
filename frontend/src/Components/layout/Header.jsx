
export default function Header() {
    return (
       <>
            <header className='header'>
                {/* Left — Logo */}
                <div className='logo'>
                ✈️ <span className='logo-text'>WanderLust</span>
                </div>
                {/* Right — Login Button*/}
                <div className='right'>
                    <button className="btn">
                        Sign In
                    </button>
                </div>
            </header>
       </>
    )
}
