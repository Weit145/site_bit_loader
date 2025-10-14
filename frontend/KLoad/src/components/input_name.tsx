// import { useState } from "react"
import './input_password.css'
import '../App.css'

export default function Input_name({children, name, setName}: {children:string, name:any, setName:any}){
    
    function handlePasswordChange(event:any){
        console.log(event.target.value)
        setName(event.target.value)
    }

    return(
        <form>
            <label htmlFor='name_input' className='input_text'>{children}</label>
            <input type="text" id='name_input' value={name} onChange={handlePasswordChange} className="input_area"/>
        </form>
    )
}