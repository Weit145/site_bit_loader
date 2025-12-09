// import { useState } from "react"
import './input.css'
import '../App.css'
import type { CSSProperties, ReactNode } from 'react';

type InputProps={
    className?:string
    children: ReactNode
    flag_error?: boolean
    type:string
    setValue: (value:string)=>void
    value: string
    onBlur?:()=>void
    touched?:boolean
    errorMessage?:string
    style?: CSSProperties
}

export default function Input({style, children, type, flag_error, setValue, value, onBlur, touched = false, errorMessage=""}: InputProps){
    function handleChange(event: React.ChangeEvent<HTMLInputElement>){
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
                    <input style={style} type={type} value={value} onChange={handleChange} onBlur={handleBlur} className={flag_error==true ? "input_area_incorrect" : "input_area" }/>
                    {touched && flag_error && <div className="error_message">{errorMessage}</div>}
                </div>
            </label>
    )
}