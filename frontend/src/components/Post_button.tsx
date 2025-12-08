import { useState } from 'react'
import defualte from "../assets/post_button.svg"
import cancel from "../assets/post_button_cancel.svg"
import "./post_button.css"
import Post_form from './post_form'


export default function Post_button (){
    const [button_flag, setButton_flag] = useState <boolean>(false);

    function Button_click(){
        if(!button_flag)setButton_flag(true);
        else setButton_flag(false)
    }

    return(
        <div>
            
            <button className='post_button' type="button" onClick={()=>Button_click()}>
                <img className='post_image_button' src={!button_flag ? defualte : cancel} alt={!button_flag ? 'post_button' : 'post_button_cancel'}/>
            </button>
            {button_flag &&
            <Post_form/>}
        </div>
    );
};