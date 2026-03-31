import { useState } from 'react'


export default function AuthModal({ onClose }) {

    const [ email, setEmail ] = useState('')
    const [ password, setPassword ] = useState('')
    const [ loading, setLoading ]  = useState(false)
    // By default give the option to sign in
    const [isLogin, setIsLogin]  = useState(true)

    function handleSubmit(){
        setLoading(true)
        try{
            onClose()
        } catch(error) {
            setError(error.message || 'Something went wrong')
        } finally {
            setLoading(false)
        }
    }

    return (    
        <div className='backdrop' onClick={onClose}>  
            {/* Modal — stop click propagating to backdrop, so that clicking any where on modal donot close it */}
            <div className='modal' onClick={e => e.stopPropagation()}>
                <h2 className='title'>{isLogin ? 'Sign In' : 'Create Account'}</h2>
                <input
                    className='input' 
                    type="text" 
                    placeholder='Email'
                    value={email}
                    onChange={ e => setEmail(e.target.value) }
                />
                <input
                    className='input' 
                    type="password" 
                    placeholder='Password'
                    value={password}
                    onChange={ e => setPassword(e.target.value) }
                />                
                <button 
                    className='submit-btn'
                    onClick={handleSubmit}
                    disabled={loading}
                >
                    {loading ? 'Please wait...' : isLogin ? 'Sign In' : 'Sign Up'}
                </button>
                <p className='toggle'>
                    {isLogin ? "Don't have an account? " : 'Already have an account? '}
                    <span
                        className='toggle-link'
                        onClick={() => { setIsLogin(!isLogin) }}
                    >
                        {isLogin ? 'Sign Up' : 'Sign In'}
                    </span>
                </p>
            </div>
        </div>
    )
}

