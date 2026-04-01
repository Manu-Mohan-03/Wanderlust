import { createContext, useState } from "react";


const AuthDetails = createContext(null)

export default function AuthContext({children}){

    const [user, setUser] = useState(null)

    function login(email,password){
        setUser({name: 'USER', email: email})
        console.log("Logged In")
    }

    function logout(){
        setUser(null)
        console.log("Logged Out")
    }

    function register(email,password){
        setUser({name: 'NEW', email: email})   
        console.log("Registered")     
    }

    return (
        <AuthDetails.Provider value={{ user, login, register, logout }}>
            {children}
        </AuthDetails.Provider>
    )
}

export { AuthDetails }
