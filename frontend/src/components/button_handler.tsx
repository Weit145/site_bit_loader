import './button_handler.css'
// import { useState, useEffect} from 'react'
export default function Button ({children , onClick, type}: { children : string, onClick: ()=>void , type:any}){
    return(
        <button className="Button" onClick={onClick} type={type} >
            {children}
        </button>
    )

}
