import axios from "axios";

import React, { useState } from "react";
import "./App.css";
import Button from "./components/button_handler";
import "./components/button_handler.css";
import Header from "./components/Header";
import Input from './components/input'

function App() {
  const [name, setName] = useState<string>("");
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [password_confirm, setPassword_confirm] = useState<string>("");

  const [flag_name_error, setFlag_name_error] = useState<boolean>(false);
  const [flag_email_error, setFlag_email_error] = useState<boolean>(false);
  const [flag_password_error, setFlag_password_error] = useState<boolean>(false);
  const [flag_password_confirm_error, setFlag_password_confirm_error] = useState<boolean>(false);

  const [touchedName, setTouchedName] = useState<boolean>(false);
  const [touchedEmail, setTouchedEmail] = useState<boolean>(false);
  const [touchedPassword, setTouchedPassword] = useState<boolean>(false);
  const [touchedPasswordConfirm, setTouchedPasswordConfirm] = useState<boolean>(false);

  const validateName = (v: string) => v.trim().length >= 3; // минимум 3 символов
  const validateEmail = (v: string) => {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(v);
  };
  const validatePassword = (v: string) => v.length >= 6; // минимум 6 символов
  const validatePasswordConfirm = (v: string, pass: string) => v === pass && v.length > 0;

function handleNameChange(v: string) {
    setName(v);
    if (touchedName) setFlag_name_error(!validateName(v));
  }
  function handleEmailChange(v: string) {
    setEmail(v);
    if (touchedEmail) setFlag_email_error(!validateEmail(v));
  }
  function handlePasswordChange(v: string) {
    setPassword(v);
    if (touchedPassword) setFlag_password_error(!validatePassword(v));
    // если подтверждение пароля уже введено, перепроверим его
    if (touchedPasswordConfirm) {
      setFlag_password_confirm_error(!validatePasswordConfirm(password_confirm, v));
    }
  }
  function handlePasswordConfirmChange(v: string) {
    setPassword_confirm(v);
    if (touchedPasswordConfirm) setFlag_password_confirm_error(!validatePasswordConfirm(v, password));
  }

  // onBlur: отмечаем touched и валидируем
  function handleNameBlur() {
    setTouchedName(true);
    setFlag_name_error(!validateName(name));
  }
  function handleEmailBlur() {
    setTouchedEmail(true);
    setFlag_email_error(!validateEmail(email));
  }
  function handlePasswordBlur() {
    setTouchedPassword(true);
    setFlag_password_error(!validatePassword(password));
  }
  function handlePasswordConfirmBlur() {
    setTouchedPasswordConfirm(true);
    setFlag_password_confirm_error(!validatePasswordConfirm(password_confirm, password));
  }


  function Button_click(type: string) {
    console.log("Button clicked", type);
    console.log("name:", name);
    console.log("password:", password);
  }

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();

    setTouchedName(true);
    setTouchedEmail(true);
    setTouchedPassword(true);
    setTouchedPasswordConfirm(true);

    const nameInvalid = !validateName(name);
    const emailInvalid = !validateEmail(email);
    const passwordInvalid = !validatePassword(password);
    const passwordConfirmInvalid = !validatePasswordConfirm(password_confirm, password);

    setFlag_name_error(nameInvalid);
    setFlag_email_error(emailInvalid);
    setFlag_password_error(passwordInvalid);
    setFlag_password_confirm_error(passwordConfirmInvalid);

    if (nameInvalid || emailInvalid || passwordInvalid || passwordConfirmInvalid) {
      // не отправляем форму — ошибки показаны пользователю
      console.log("Validation failed, not sending. Flags:", {
        nameInvalid,
        emailInvalid,
        passwordInvalid,
        passwordConfirmInvalid,
      });
      return;
    }

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
          params.toString(),

          {
            headers: {
              "Content-Type": "application/x-www-form-urlencoded",
            },
          }
        );
        console.log("Ответ сервера:", response.data);
      } 
      catch (error: any) {
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
              type="email"
              value={email}
              setValue={handleEmailChange}
              flag_error={flag_email_error}
              onBlur={handleEmailBlur}
              touched={touchedEmail}
              errorMessage="Введите корректный email адрес"
            >Почта</Input>

            <Input
              type="password"
              value={password}
              setValue={handlePasswordChange}
              flag_error={flag_password_error}
              onBlur={handlePasswordBlur}
              touched={touchedPassword}
              errorMessage="Пароль должен содержать не менее 6 символов"
            >Пароль</Input>

            <Input
              type="password"
              value={password_confirm}
              setValue={handlePasswordConfirmChange}
              flag_error={flag_password_confirm_error}
              onBlur={handlePasswordConfirmBlur}
              touched={touchedPasswordConfirm}
              errorMessage="Пароли не совпадают"
            >Подтвердите пароль</Input>

            <Button onClick={() => Button_click("b")} type={"submit"} flag_disabled={flag_email_error || flag_name_error || flag_password_confirm_error || flag_password_error}>
              Авторизоваться
            </Button>
            <Button onClick={() => Button_click("b")} type={"button"} flag_disabled={false}>
              Регистрация
            </Button>
          </form>
        </div>
      </main>
    </div>
  );

}
export default App
