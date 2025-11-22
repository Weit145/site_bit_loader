// import axios from "axios";

import  { useState, useEffect } from "react";
import "./App.css";
import "./components/button_handler.css";
import Header from "./components/Header";
import { getAccessToken, refreshOnce } from "./api";


export default function App() {
  const [access, setAccess] = useState<string | null>(() => getAccessToken());

  useEffect(() => {
    let mounted = true;
    refreshOnce()
      .then((newAccess: any) => {
        if (!mounted) return;
        setAccess(newAccess ?? getAccessToken());
      })
      .catch(() => {
        if (mounted) setAccess(getAccessToken());
      });
    return () => { mounted = false; };
  }, []);

  const content = [
    {title:"Aaaa", body:"asdaadasd", name_img:"default.png", user_name: "weit", id:0},
    {title:"Bbbbbb", body:"oajsdasdakmda", name_img:"default.png", user_name: "fugi", id:1},
    {title:"CCcc", body:"pasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopaincapasikdopainca", name_img:"default.png", user_name: "coloss", id:2},
    {title:"DDDDdddd", body:"qwhbdzxnzmlcdm", name_img:"default.png", user_name: "mifugi", id:3},
    {title:"EEeeeee", body:"Wdjznxjc z q", name_img:"default.png", user_name: "fkxcmzxugi", id:4},
    {title:"Ffffff", body:"ffAsjimcacicnoqc", name_img:"default.png", user_name: "lol", id:5}
  ];

  return (
    <div>

      <Header />

      <main className="content_box">
         {/* <img className="image" src={"../public/default.png"}/> */}

          {content.map((option, index) => (
            <div className="content_text" key={index}>
              <div className="lable_text" >{option.title}</div>
              <span><img className="image" src="../public/default.png"/></span>
              <span style={{color:"red"}}>  {option.user_name + "@kload: " }</span>
              {option.body}
            </div>
          ))}
          <span>{access}</span>
      </main>


    </div>
  );

}