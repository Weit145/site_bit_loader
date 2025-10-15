// import { useState } from "react"
import './input_password.css'
import '../App.css'

export default function Input_password({children, password, setPassword, name}: {children:string, password:any, setPassword:any, name:string}){
    let test:string
    if (password=='1'){
        test='good'
    }
    else{
        test = 'bad'
    }
    function handlePasswordChange(event:any){
        console.log(event.target.value)
        setPassword(event.target.value)
    }

    return(
        
            <label htmlFor='form_row'>
                <span className='input_text'>{children}</span>
                <input type="password" id='password_input' value={password} name={name} onChange={handlePasswordChange} className={password=='2' ? "input_area" : "input_area_incorrect"}/>
                <span className='input_text'>{test}</span>
            </label>
    )
}