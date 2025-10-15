import axios from "axios";

import React, { useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
// import Input_name from './components/input_name'
// import Input_password from './components/input_password'
// import Input_password_pod from './components/input_password_pod'

function App() {
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");

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
            name,
            password,
            scope: "",
            client_id: "",
            client_secret: "",
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

          <form onSubmit={handleSubmit} noValidate>
            <div>
              <label>
                Email:
                <input
                  type="name"
                  name="name"
                  value={name}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setName(e.target.value)
                  }
                />
              </label>
            </div>

            <div>
              <label>
                Password:
                <input
                  type="password"
                  name="password"
                  value={password}
                  onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                    setPassword(e.target.value)
                  }
                />
              </label>
            </div>

            <div style={{ marginTop: 12 }}>
              <input type="submit" value="Log in" />
              <Button onClick={() => Button_click("b")} type={"button"}>
                Авторизоваться
              </Button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );

}
export default App
