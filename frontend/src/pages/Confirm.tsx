import  {useEffect, useState } from "react";
import "./Pages.css";
import Header from "../components/Header";
import {useLocation,useNavigate } from "react-router";
import api from "../api";
import { setAccessToken, getAccessToken} from "../api";



export default function Confirm() {
  // const [tokenPod, setTokenPod] = useState<string | null>(null);
  const location = useLocation();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {

    const params = new URLSearchParams(location.search);
    const token = params.get("token_pod");
    if (token){
      // setAccessToken(token);
      (async() =>{
        setLoading(true);
        setError(null);
        try {
          const response = await api.get(
            "/user/registration/confirm/",{
          params: { token_pod: token },
          // headers: { Authorization: undefined } // на всякий случай
        });

        
        const newAccess = response.data?.access_token;
        if (newAccess) setAccessToken(newAccess);
          // setAccessToken(response.data?.access_token || null);
          if(getAccessToken()!=null){
            navigate("/");
            return;
          }
        } catch (error: any) {
          console.error("Ошибка при отправке данных:", error.response?.data || error.message);
          setError("Ошибка при подтверждении. Проверьте консоль.");
          return;
        } finally {
          setLoading(false);  
        }
      })();
    }
    
  }, [location.search, navigate]);  
  
  return (
    <div>
      <Header />
      <main>
        <div className="content_box">
          <h1 className="content_text"> Подтверждение регистрации</h1>
          <h2 className="content_text"><span className="content_text_root">root@:~$</span> Здесь скоро будет форум</h2>
          
          <h5>Access token: {getAccessToken()}</h5>

          {loading && <p>Отправка...</p>}
          {error && <p style={{ color: "red" }}>{error}</p>}

        </div>
      </main>
    </div>
  );

}
