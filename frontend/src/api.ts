import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
});

let accessToken: string | null = null;
export function setAccessToken(token: string | null) { accessToken = token; }
export function getAccessToken() { return accessToken; }

api.interceptors.request.use((config) => {
    if (accessToken) {
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
});

let isRefreshing = false;
let refreshPromise: Promise<any> | null = null;
export async function refreshOnce(){
    if(isRefreshing)return refreshPromise;
    isRefreshing = true;
    refreshPromise = api.post("/auth/refresh")
    .then(res =>{
        const newAccess=res.data?.access_token;
        if(newAccess)setAccessToken(newAccess);
        return newAccess;
    })
    .finally(()=>{
        isRefreshing = false;
        refreshPromise = null;
    });
    return refreshPromise;
}

api.interceptors.response.use(
    res=>res,
    async (err) => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
        original._retry = true;
        try{
            await refreshOnce();
            return api(original);
        } catch(e){
            setAccessToken(null);
            //Logout or redirect to login page can be handled here
        }
    }
    return Promise.reject(err);
    }
);
export default api;