import { useContext, useState, useEffect } from "react"
import { AuthDetails } from "../context/AuthContext"
import { useNavigate } from "react-router"
import { userAPI } from "../services/api"



export default function AccountPage() {

  const { user, updateUser, logout } = useContext(AuthDetails)
  const [profile, setProfile] = useState({
    username: '',
    email: '',
    city: '',
    country: '',
  })
  const [passwords, setPasswords] = useState({
    current: '',
    new: ''
  })
  const navigate = useNavigate()

  // Redirect if not logged in
  useEffect(() => {
    if (!user) navigate('/')
  }, [user])

  // Populate form from current user
  useEffect(() => {
    if (user) {
      setProfile({
        username: user.username ?? '',
        email: user.email ?? '',
        city: user?.city_details?.name ?? '',
        country: user.country ?? '',
      })
    }
  }, [user])

  const userDefault = () => {
    return {
      id: user.id,
      username: user?.username ?? null,
      email: user?.email ?? null,
      role: user.role,
      city: user?.city ?? null,
      country: user?.country ?? null,
      dark_mode: user.dark_mode ?? false,
      map_mode: user.map_mode ?? false,
      date_tolerance: user.date_tolerance ?? null,
      password: null
    }
  }

  async function handleProfileSave() {
    try {
      const userUpdate = { ...userDefault(), ...profile }
      const updated = await userAPI.update(userUpdate)
      updateUser(updated)
    } catch (err) {
      console.error(err)
    } finally {
      //
    }
  }

  async function handleChangePassword() {
    if (passwords.current && passwords.new) {
      try {
        const userUpdate = { ...userDefault(), password: passwords.new }
        await userAPI.update(userUpdate)
        setPasswords({ current: '', next: '', confirm: '' })
      } catch (err) {
        console.error(err)
      } finally {
        //
      }
    } else {
      // Error message
    }
  }

  async function handleDeleteAccount() {
    try {
      await userAPI.delete(user.id)
      logout()
      navigate('/')
    } catch (err) {
      console.error(err)
    } finally {
      //
    }

  }

  if (!user) return null

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
            <div className='readonly'>{user.email}</div>
          </div>

          {/* Username */}
          <div className='field-group'>
            <label className='label'>Username</label>
            <input
              className='input'
              type="text"
              placeholder="Enter a username"
              value={profile.username}
              onChange={e => setProfile(prev => ({ ...prev, username: e.target.value }))}
            />
          </div>

          {/* City */}
          <div className='field-group'>
            <label className='label'>City</label>
            <input
              className='input'
              type="text"
              placeholder="Your city"
              value={profile.city}
              onChange={e => setProfile(prev => ({ ...prev, city: e.target.value }))}
            />
          </div>

          {/* Country */}
          <div className='field-group'>
            <label className='label'>Country</label>
            <input
              className='input'
              type="text"
              placeholder="Your country"
              value={profile.country}
              onChange={e => setProfile(prev => ({ ...prev, country: e.target.value }))}
            />
          </div>

          <div className='card-footer'>
            <button
              className='save-button'
              onClick={handleProfileSave}
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
              value={passwords.current}
              onChange={e => setPasswords(prev => ({ ...prev, current: e.target.value }))}
            />
          </div>
          <div className='field-group'>
            <label className='label'>New Password</label>
            <input
              className='input'
              type="password"
              placeholder="password"
              value={passwords.new}
              onChange={e => setPasswords(prev => ({ ...prev, new: e.target.value }))}
            />
          </div>

          <div className='card-footer'>
            <button
              className='save-button'
              onClick={handleChangePassword}
            >
              Update Password
            </button>
          </div>

        </div>

        {/* Delete User - Danger Zone*/}
        <div className="danger-card">
          <h2 className='danger-title'>Danger Zone</h2>
          <div className="danger-row">
            <div>
              <p className='danger-label'>Delete Account</p>
              <p className='danger-subtext'>
                Permanently delete your account and all saved trips. This cannot be undone.
              </p>
            </div>
            <button className='delete-button' onClick={handleDeleteAccount}>
              Delete Account
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}







