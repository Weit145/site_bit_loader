// import { useState } from "react"
import './input_password.css'
import '../App.css'

export default function input_password({children, type, password_confirm, setPassword, password}: {children:string, type:string, password_confirm:string, setPassword:(any), password:string}){
    function handlePasswordChange(event:any){
        console.log(event.target.value)
        setPassword(event.target.value)
    }


    return(
        
            <label htmlFor='form_row'>
                <div>
                    <span className='input_text'>{children}</span>
                </div>
                <div>
                    <input type={type} value={password} onChange={handlePasswordChange} className={password==password_confirm ? "input_area" : "input_area_incorrect"}/>
                </div>
            </label>
    )
}