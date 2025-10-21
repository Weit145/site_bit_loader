import './button_handler.css'
// import { useState, useEffect} from 'react'
export default function Button ({children , onClick, type, flag_disabled}: { children : string, onClick: ()=>void , type:any,  flag_disabled:boolean}){
    return(
        <button className="Button" onClick={onClick} type={type} disabled={flag_disabled} >
            {children}
        </button>
    )

}
