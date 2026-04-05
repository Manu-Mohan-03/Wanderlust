import { createContext, useState } from "react";
import { authAPI } from "../services/api";


const AuthDetails = createContext(null)

export default function AuthContext({children}){

    const [user, setUser] = useState(null)

    async function login(email,password){
        // const res = await authAPI.login({ email, password })
        // const user = res.data
        const user = await authAPI.login({ email, password })
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
        const user = await authAPI.register({ email, password })
        setUser({...user, name: user?.username?? 'ANON'})  
        console.log("Registered")   
        return user          
    }

    return (
        <AuthDetails.Provider value={{ user, login, register, logout }}>
            {children}
        </AuthDetails.Provider>
    )
}

export { AuthDetails }
