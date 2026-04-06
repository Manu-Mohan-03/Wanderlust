


export default function AccountPage() {
  return (
    <div className="page">
      <div className="account-container">

        {/* Page header */}
        <div className='page-header'>
          <h1 className='title'>My Account</h1>
          <button className='back-button' onClick={() => navigate('/')}>
            ← Back to Map
          </button>
        </div>

        {/* ── Profile section ── */}
        <div className='card'>
          <h2 className='section-title'>Profile</h2>

          {/* Email — display only */}
          <div className='field-group'>
            <label className='label'>Email</label>
            <div className='readonly'>email@email.com</div>
          </div>

          {/* Username */}
          <div className='field-group'>
            <label className='label'>Username</label>
            <input
              className='input'
              type="text"
              placeholder="Enter a username"
            />
          </div>

          {/* City */}
          <div className='field-group'>
            <label className='label'>City</label>
            <input
              className='input'
              type="text"
              placeholder="Your city"
            />
          </div>

          {/* Country */}
          <div className='field-group'>
            <label className='label'>Country</label>
            <input
              className='input'
              type="text"
              placeholder="Your country"
            />
          </div>       

          <div className='card-footer'>
            <button
              className='save-button'
            >
              Save Changes
            </button>
          </div>
        </div>

        {/* ── Change password section ── */}
        <div className='card'>
          <h2 className='section-title'>Change Password</h2>
          <div className='field-group'>
            <label className='label'>Current Password</label>
            <input
              className='input'
              type="password"
              placeholder="Enter current password"
            />
          </div> 
          <div className='field-group'>
            <label className='label'>New Password</label>
            <input
              className='input'
              type="password"
              placeholder="password"
            />
          </div>    

          <div className='card-footer'>
            <button
              className='save-button'
            >
              Update Password
            </button>
          </div>

        </div>

      </div>
    </div>
  )
}





