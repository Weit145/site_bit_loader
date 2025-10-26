import axios from "axios";

import { useState } from "react";
import "./Pages.css";
import Button from "../components/button_handler";
import "../components/button_handler.css";
import Header from "../components/Header";
import Input from '../components/input';
import { Link } from "react-router";

export default function Login() {
  const [name, setName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [flag_name_error, setFlag_name_error] = useState<boolean>(false);
  const [flag_password_error, setFlag_password_error] = useState<boolean>(false);

  const [touchedName, setTouchedName] = useState<boolean>(false);
  const [touchedPassword, setTouchedPassword] = useState<boolean>(false);

  const validateName = (v: string) => v.trim().length >= 3; // минимум 3 символов
  const validatePassword = (v: string) => v.length >= 6; // минимум 6 символов

function handleNameChange(v: string) {
    setName(v);
    if (touchedName) setFlag_name_error(!validateName(v));
  }
  function handlePasswordChange(v: string) {
    setPassword(v);
    if (touchedPassword) setFlag_password_error(!validatePassword(v));
  }

  // onBlur: отмечаем touched и валидируем
  function handleNameBlur() {
    setTouchedName(true);
    setFlag_name_error(!validateName(name));
  }
  function handlePasswordBlur() {
    setTouchedPassword(true);
    setFlag_password_error(!validatePassword(password));
  }


  function Button_click(type: string) {
    console.log("Button clicked", type);
    console.log("name:", name);
    console.log("password:", password);
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setTouchedName(true);
    setTouchedPassword(true);

    const nameInvalid = !validateName(name);
    const passwordInvalid = !validatePassword(password);

    setFlag_name_error(nameInvalid);
    setFlag_password_error(passwordInvalid);

    if (nameInvalid || passwordInvalid) {
      // не отправляем форму — ошибки показаны пользователю
      console.log("Validation failed, not sending. Flags:", {
        nameInvalid,
        passwordInvalid,
      });
      return;
    }

    const params = new URLSearchParams({
      username : name,
      password : password,
    })
    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/users/",
        {
          username: name,
          password: password,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      console.log("Ответ сервера:", JSON.stringify(response.data, null, 2));
    } catch (error: any) {
      console.error("Ошибка при отправке данных:", error.response?.data || error.message);
    }
      console.log("Submit:", { name, password });
      // alert(`Отправлено:\nEmail: ${name}\nPassword: ${password}`);

  
    
  }

  return (
    <div>

      <Header />

      <main>
        <div className="form_box">
          <h1 className="form_text">Авторизация</h1>

          <form onSubmit={handleSubmit} noValidate className="form_button_box">

            <Input
              type="username"
              value={name}
              setValue={handleNameChange}
              flag_error={flag_name_error}
              onBlur={handleNameBlur}
              touched={touchedName}
              errorMessage="Имя должно содержать не менее 3 символов"
            >Логин</Input>

            <Input
              type="password"
              value={password}
              setValue={handlePasswordChange}
              flag_error={flag_password_error}
              onBlur={handlePasswordBlur}
              touched={touchedPassword}
              errorMessage="Пароль должен содержать не менее 6 символов"
            >Пароль</Input>

            <Button onClick={() => Button_click("b")} type={"submit"} flag_disabled={flag_name_error || flag_password_error}>
              Подтвердить
            </Button>
            <Link to="/register">
              <Button onClick={() => Button_click("b")} type={"button"} flag_disabled={false}>
                Зарегистрироваться
              </Button>
            </Link>
          </form>
        </div>
      </main>
    </div>
  );

}
