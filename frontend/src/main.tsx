import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import Login from "./pages/Login.tsx"
import Register from "./pages/Register.tsx"
import Confirm from './pages/Confirm.tsx' 
import Profile from './pages/Profile.tsx'

import {BrowserRouter, Route, Routes} from "react-router"


// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <link
//       href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
//       rel="stylesheet"
//     ></link>
//     <App />
//   </StrictMode>,
// )
createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <link
        href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
        rel="stylesheet"
      ></link>
      <Routes>
          <Route path='/' element={<App/>}/>
          <Route path='/login' element ={<Login/>}/>
          <Route path='/register' element={<Register/>}/>
          <Route path='/confirm' element={<Confirm/>}/>
          <Route path='/profile' element={<Profile/>}/>
      </Routes>
    
    </BrowserRouter>
  </StrictMode>
)
