// import { useState } from "react"
import './input.css'
import '../App.css'

export default function Input({children, type, flag_error, setValue, value, onBlur, touched = false, errorMessage=""}: {children:string, type:string, flag_error:boolean, setValue:(any), value:string, onBlur?:()=>void, touched?:boolean, errorMessage?:string}){
    function handleChange(event:any){
        console.log(event.target.value)
        setValue(event.target.value)
    }
    function handleBlur() {
    if (onBlur) onBlur();
    }

    return(
        
            <label htmlFor='form_row'>
                <div>
                    <span className='input_text'>{children}</span>
                </div>
                <div>
                    <input type={type} value={value} onChange={handleChange} onBlur={handleBlur} className={flag_error==true ? "input_area_incorrect" : "input_area" }/>
                    {touched && flag_error && <div className="error_message">{errorMessage}</div>}
                </div>
            </label>
    )
}