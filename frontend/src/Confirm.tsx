import axios from "axios";

import  {useEffect, useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import { Link, useLocation } from "react-router";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  withCredentials: true, // важно: браузер отправит HttpOnly cookie
});

export default function Confirm() {
  const [tokenPod, setTokenPod] = useState<string | null>(null);
  const location = useLocation();
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token_pod");
    if (token) setTokenPod(token);
  }, [location.search]);

  
  function Button_click(type: string) {
    console.log("Button clicked", type);
  }

  

async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    try {
      const response = await api.get(
        "http://127.0.0.1:8000/user/registration/confirm",
        {
          params: { token_pod: tokenPod },
          
        }
      );

      console.log("Ответ сервера:", JSON.stringify(response.data, null, 2));
      alert("Данные успешно отправлены!");
    } catch (error: any) {
      console.error("Ошибка при отправке данных:", error.response?.data || error.message);
      alert("Ошибка при отправке данных. Пожалуйста, попробуйте еще раз.");

    }
      alert("Данные успешно отправлены!");
      // alert(`Отправлено:\nEmail: ${name}\nPassword: ${password}`);

  
    
  }

  return (
    <div>

      <Header />

      <main>
        <div className="content_box">
          <h1 className="content_text">Тема треда</h1>
          <h2 className="content_text"><span className="content_text_root">root@:~$</span> Здесь скоро будет форум</h2>
          <form onSubmit={handleSubmit} noValidate>
            {/* <Link to ="/"> */}
              <Button onClick={() => Button_click("b")} type={"submit"} flag_disabled={false}>
              Подтвердить регистрацию
              </Button>
            {/* </Link> */}
          </form>
        </div>
      </main>
    </div>
  );

}
