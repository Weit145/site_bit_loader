// import axios from "axios";

import  { useState, useEffect } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import { Link } from "react-router";
import api from "./api";
import { getAccessToken, refreshOnce } from "./api";


export default function App() {
  const [access, setAccess] = useState<string | null>(() => getAccessToken());

  useEffect(() => {
    // Вызываем один раз при монтировании — получим access через refresh token (куки)
    let mounted = true;
    refreshOnce()
      .then((newAccess: any) => {
        if (!mounted) return;
        // refreshOnce в вашем api возвращает промис, который резолвится в newAccess (или undefined)
        setAccess(newAccess ?? getAccessToken());
      })
      .catch(() => {
        if (mounted) setAccess(getAccessToken());
      });
    return () => { mounted = false; };
  }, []);

  function Button_click(type: string) {
    console.log("Button clicked", type);
  }

  
  return (
    <div>

      <Header />

      <main>
        <div className="content_box">
          <h1 className="content_text">Тема треда</h1>
          <h2 className="content_text"><span className="content_text" style={{color:"red"}}>root@:~$</span> Здесь скоро будет форум</h2>
          <span>{access}</span>
        </div>
      </main>
    </div>
  );

}
