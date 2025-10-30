// import axios from "axios";

// import  { useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import { Link } from "react-router";


export default function App() {
  
  function Button_click(type: string) {
    console.log("Button clicked", type);
  }

  
  return (
    <div>

      <Header />

      <main>
        <div className="content_box">
          <h1 className="content_text">Тема треда</h1>
          <h2 className="content_text"><span className="content_text_root">root@:~$</span> Здесь скоро будет форум</h2>
          <Link to ="/register">
              <Button onClick={() => Button_click("b")} type={"button"} flag_disabled={false}>
              Регистрация
              </Button>
            </Link>
            <Link to ="/login">
              <Button onClick={() => Button_click("b")} type={"button"} flag_disabled={false}>
              Войти
              </Button>
            </Link>
            <Link to ="/confirm">
              <Button onClick={() => Button_click("b")} type={"button"} flag_disabled={false}>
              Подтвердите регистрацию
              </Button>
            </Link>
        </div>
      </main>
    </div>
  );

}
