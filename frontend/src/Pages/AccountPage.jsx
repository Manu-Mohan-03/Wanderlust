


export default function AccountPage() {
  return (
    <div className="xxx">
      <div className="xxx">

        {/* Page header */}
        <div className=''>
          <h1 className=''>My Account</h1>
          <button className='' onClick={() => navigate('/')}>
            ← Back to Map
          </button>
        </div>

        {/* ── Profile section ── */}
        <div className=''>
          <h2 className='section-title'>Profile</h2>

          {/* Email — display only */}
          <div className=''>
            <label className=''>Email</label>
            <div className=''>email@email.com</div>
          </div>

          {/* Username */}
          <div className=''>
            <label className=''>Username</label>
            <input
              className=''
              type="text"
              placeholder="Enter a username"
            />
          </div>

          {/* City */}
          <div className=''>
            <label className=''>City</label>
            <input
              className=''
              type="text"
              placeholder="Your city"
            />
          </div>

          {/* Country */}
          <div className=''>
            <label className=''>Country</label>
            <input
              className=''
              type="text"
              placeholder="Your country"
            />
          </div>       

          <div className=''>
            <button
              className=''
            >
              Save Changes
            </button>
          </div>
        </div>

        {/* ── Change password section ── */}
        <div className=''>
          <h2 className='section-title'>Change Password</h2>
          <div className=''>
            <label className=''>Current Password</label>
            <input
              className=''
              type="password"
              placeholder="Enter current password"
            />
          </div> 
          <div className=''>
            <label className=''>New Password</label>
            <input
              className=''
              type="password"
              placeholder="password"
            />
          </div>    

          <div className=''>
            <button
              className=''
            >
              Update Password
            </button>
          </div>

        </div>
        
      </div>
    </div>
  )
}