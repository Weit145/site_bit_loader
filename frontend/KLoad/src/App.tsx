// import { useState, useEffect} from 'react'

import './App.css'
import './components/button_handler'
import Button from './components/button_handler'
import Header from './components/Header'
import Input_name from './components/input_name'
import Input_password from './components/input_password'
import {useState} from 'react'


// function Input_custom({text, type_text}: { text: string, type_text:string}){
//   const test ='';
//   return (
//     <>
//       <div className='content_text'>{text}</div>
//       <input type={type_text} value={test}/>
//     </>
//   )
// }


function App() {
  const [password, setPassword] = useState('')
  const [password_pod, setPassword_pod] = useState('')
  const [name, setName] = useState('')

  function Button_click(type:string){
    console.log('Button clicked',type)
    console.log(password)
    console.log(password_pod)
  } 

  return (
    <div>
      <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet"></link>
      <Header/>
      <main>
        <div className='content_box'> 
          <h1 className='content_text'>Регистрация</h1>
         
          <Input_name name ={name} setName={setName}>Имя</Input_name>
          <Input_password password={password} setPassword={setPassword}>Пароль</Input_password>
          <Input_password password={password_pod} setPassword={setPassword_pod}>Подтвердите пароль</Input_password>
          <form>
            <input type='submit'/>
            {/* <input type='color'/>
            <input type='datetime-local'/> */}
            {/* <input type='file'/> */}
            <input type='reset'/>
          </form>
          <div className='button_box'>
            
            <Button onClick={()=> Button_click('a')}>Подтвердить</Button>
            <Button onClick={()=> Button_click('b')}>Авторизоваться</Button>
          </div>
        </div>
        
      </main>
    </div>
  )
}

export default App
