import  {useEffect, useState } from "react";
import "./Pages.css";
import Header from "../components/Header";
import { Link, useLocation,useNavigate } from "react-router";
import api from "../api";
import { setAccessToken as setTokenPod } from "../api";


export default function Confirm() {
  // const [tokenPod, setTokenPod] = useState<string | null>(null);
  const location = useLocation();
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const token = params.get("token_pod");
    if (token) setTokenPod(token);
  }, [location.search]);
  

async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const navigate = useNavigate();

    try {
      const response = await api.get(
        "http://127.0.0.1:8000/user/registration/confirm",
        // {
        //   params: { token_pod: tokenPod },
          
        // }
      );
      try{
        const Response_token = await api.post("/auth/refresh");
        if (Response_token.data?.access_token){
          setTokenPod(Response_token.data.access_token);
          navigate("/");
          return;
        }
        else{
          const me = await api.get("/auth/me");
          if (me.data?.username){
            navigate("/");
            return;
          }
        }
      }
      catch(refreshError){
        console.error("Ошибка при обновлении токена:", refreshError);
      }
      setTokenPod(response.data?.access_token || null);
      alert(JSON.stringify(response.data, null, 2));
      console.log("Ответ сервера:", JSON.stringify(response.data, null, 2));
    } catch (error: any) {
      console.error("Ошибка при отправке данных:", error.response?.data || error.message);
      alert("Ошибка при отправке данных. Пожалуйста, попробуйте еще раз.");
    }
  }
  handleSubmit(null as any);
  return (
    <div>
      <Header />
      <main>
        <div className="content_box">
          <h1 className="content_text">Тема треда</h1>
          <h2 className="content_text"><span className="content_text_root">root@:~$</span> Здесь скоро будет форум</h2>
          <form onSubmit={handleSubmit} noValidate>
            {/* <Link to ="/"> */}
              {/* <Button onClick={() => Button_click("b")} type={"submit"} flag_disabled={false}>
              Подтвердить регистрацию
              </Button> */}
            {/* </Link> */}

          </form>
        </div>
      </main>
    </div>
  );

}
