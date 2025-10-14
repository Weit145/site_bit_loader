import './Header.css'
import './button_handler'
import menu_option from '../assets/menu_option.svg'
// import Button from './button_handler'
export default function Header(){
    // function pod_menu(){
    //     return(
    //         <div>

    //         </div>
    //     )
    // }
    return(
        <header>
            <div className='menu_box'>
                <img className='menu_option' src = {menu_option} alt={'menu option'}/>
                <h1 className='menu_text'>KLoad</h1>
            </div>
        </header>
    )
}