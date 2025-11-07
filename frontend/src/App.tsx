// import axios from "axios";

// import  { useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import { Link } from "react-router";
import api from "./api";
import { getAccessToken } from "./api";


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
          <span>{getAccessToken()}</span>
        </div>
      </main>
    </div>
  );

}
