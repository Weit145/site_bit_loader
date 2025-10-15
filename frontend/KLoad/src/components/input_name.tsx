// import { useState } from "react"
import './input_password.css'
import '../App.css'

export default function Input_name({children, value, setName, name }: {children:string, value:any, setName:any, name:string}){
    
    function handlePasswordChange(event:any){
        console.log(event.target.value)
        setName(event.target.value)
    }

    return(
        <>
            <label htmlFor='name_input' className='input_text'>{children}</label>
            <input type="text" name={name} id='name_input' value={value} onChange={handlePasswordChange} className="input_area"/>
         </>
    )
}