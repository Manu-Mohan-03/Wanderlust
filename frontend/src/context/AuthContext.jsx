import { createContext, useState } from "react";
import { authAPI } from "../services/api";


const AuthDetails = createContext(null)

export default function AuthContext({children}){

    const [user, setUser] = useState(null)

    async function login(email,password){
        setUser({name: 'USER', email: email})
        console.log("Logged In")
    }

    function logout(){
        setUser(null)
        console.log("Logged Out")
    }

    async function register(email,password){
        const res = await authAPI.register({ email, password })
        const user = res.data
        setUser({...user, name: user?.name?? 'ANON'})   
        console.log("Registered")             
    }

    return (
        <AuthDetails.Provider value={{ user, login, register, logout }}>
            {children}
        </AuthDetails.Provider>
    )
}

export { AuthDetails }
