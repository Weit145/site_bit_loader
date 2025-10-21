import axios from "axios";

import React, { useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import Input_password from './components/input_password'

function App() {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [password_confirm, setPassword_confirm] = useState<string>("");


  function Button_click(type: string) {
    console.log("Button clicked", type);
    console.log("name:", name);
    console.log("password:", password);
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const params = new URLSearchParams({
      username : name,
      password : password,
      scope:"",
      client_id:"",
      client_secret:"",
    })
    try{
      const response = await axios.post(
          "http://127.0.0.1:8000/users/",
          {
            params,
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );
        console.log("Ответ сервера:", response.data);
      } catch (error: any) {
        console.error("Ошибка при отправке данных:", error);
      }
  
    console.log("Submit:", { name, password });
    alert(`Отправлено:\nEmail: ${name}\nPassword: ${password}`);
    }

  return (
    <div>

      <Header />

      <main>
        <div className="content_box">
          <h1 className="content_text">Регистрация</h1>

          <form onSubmit={handleSubmit} noValidate className="button_box">

            <Input_password
              type="username"
              password={name}
              setPassword={setName}
              password_confirm={name}
            >Логин</Input_password>

            <Input_password
              type="email"
              password={email}
              setPassword={setEmail}
              password_confirm={email}
            >Почта</Input_password>

            <Input_password
              type="password"
              password={password}
              setPassword={setPassword}
              password_confirm={password}
            >Пароль</Input_password>

            <Input_password
              type="password"
              password={password_confirm}
              setPassword={setPassword_confirm}
              password_confirm={password}
            >Подтвердите пароль</Input_password>

            <Button onClick={() => Button_click("b")} type={"submit"}>
              Авторизоваться
            </Button>
            <Button onClick={() => Button_click("b")} type={"button"}>
              Регистрация
            </Button>
          </form>
        </div>
      </main>
    </div>
  );

}
export default App
