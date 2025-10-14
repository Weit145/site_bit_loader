import './button_handler.css'
// import { useState, useEffect} from 'react'
export default function Button ({children , onClick}: { children : string, onClick: ()=>void }){
    return(
        <button className="Button" onClick={onClick} >
            {children}
        </button>
    )

}
