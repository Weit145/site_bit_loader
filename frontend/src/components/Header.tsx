import './Header.css'
import './button_handler'
import menu_option from '../assets/menu_option.svg'
import menu_option_active from '../assets/menu_option_active.svg'
import { Link } from 'react-router'
import { useState } from 'react'


export default function Header(){
    const [button_flag, setButton_flag] = useState <Boolean>(false);

    function Button_click(){
        if(!button_flag)setButton_flag(true);
        else setButton_flag(false)
    }
    const menuButtons = [
        { label: "Профиль", path: "/profile" },
        { label: "Домой", path: "/" },
        { label: "Войти", path: "/login" },
        { label: "Регистрация", path: "/register" }
    ];

    return(
        <header>

            <div className='menu_box'>
                {/* <input type="image" className='menu_option' src = {button_flag? menu_option_active : menu_option} alt={button_flag? 'menu_option_active' : 'menu option'} onClick={()=>Button_click()}/> */}
                <button type="button" onClick = {()=>Button_click()} className='menu_option'>
                    <img src = {button_flag? menu_option_active : menu_option} alt={button_flag? 'menu_option_active' : 'menu option'} className='menu_option_image'/>

                </button>

                {button_flag && (
                    <div className='option_box'>
                        {menuButtons.map((option, index) => (
                            <Link
                                key={index}
                                to={option.path}
                                className="menu_option_item"
                                onClick={() => setButton_flag(false)} // Закрываем меню при клике
                            >
                                {option.label}
                            </Link>
                        ))}
                    </div>
                )}
                {/* <input type="image" className='menu_option' src = {menu_option} alt={'menu option'}/> */}
                    {/* <h1 className='menu_text'>KLoad</h1> */}
                <Link to="/" className='menu_text_button'>
                    KLoad

                </Link>
            </div>
        </header>
    )
}