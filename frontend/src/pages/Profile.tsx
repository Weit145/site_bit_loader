import api from "../api";
import "./Pages.css"
import Header from "../components/Header";
import Button from "../components/button_handler";
import { Link } from "react-router-dom";
import type React from "react";
export default function Profile (){
    return(
        <div>
            <Header />
            <main>
                <div className = "form_box">
                    <h1 className="form_text">Профиль</h1>
                    <img src="../../public/vite.svg" alt="Default_photo" width={"200px"} height={"200px"}/>

                </div>
            </main>
        </div>
    )
}