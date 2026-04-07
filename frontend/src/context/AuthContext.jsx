import { createContext, useEffect, useState } from "react";
import { userAPI } from "../services/api";


const AuthDetails = createContext(null)

export default function AuthContext({children}){

    const [user, setUser] = useState(null)
    const [loading, setLoading] = useState(true)

    async function login(email,password){
        // const res = await authAPI.login({ email, password })
        // const user = res.data
        const user = await userAPI.login({ email, password })
        setUser({...user, name: user?.username?? 'Anon'})
        console.log("Logged In:")
        return user
    }

    function logout(){
        setUser(null)
        console.log("Logged Out")
    }

    async function register(email,password){
        // const res = await authAPI.register({ email, password })
        // const user = res.data
        const user = await userAPI.register({ email, password })
        setUser({...user, name: user?.username?? 'ANON'})  
        console.log("Registered")   
        return user          
    }

    // Updates local user state after profile change
    function updateUser(updatedUser){
        const merged = {...user, ...updatedUser}
        setUser(merged)
    }

    // useEffect(() => {
    //     setLoading(false)
    // },[])

    return (
        <AuthDetails.Provider value={{ user, login, register, logout, updateUser }}>
            {children}
        </AuthDetails.Provider>
    )
}

export { AuthDetails }
