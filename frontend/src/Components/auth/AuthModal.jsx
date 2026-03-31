import React from 'react'

export default function AuthModal({ onClose }) {
  return (    
    <div className='backdrop' onClick={onClose}>  
        {/* Modal — stop click propagating to backdrop, so that clicking any where on modal donot close it */}
        <div className='modal' onClick={e => e.stopPropagation()}>
            <h2>Sign In / Create Account</h2>
        </div>
    </div>
  )
}

