import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
});

let accessToken: string | null = null;
export function setAccessToken(token: string | null) { accessToken = token; }
export function getAccessToken() { return accessToken; }

api.interceptors.request.use((config) => {
    if (config.url !== "/user/auth/refresh" && accessToken) {
        config.headers = config.headers || {};
        config.headers.Authorization = `Bearer ${accessToken}`;
    }
    
    return config;
});

let isRefreshing = false;
let refreshPromise: Promise<any> | null = null;
export async function refreshOnce(){
    console.log("Refreshing token...");
    if(isRefreshing) return refreshPromise;
    isRefreshing = true;
    refreshPromise = api.get("/user/auth/refresh/" , { withCredentials: true })
    .then(res => {
        console.log("Refresh response:", res.data);
        const newAccess = res.data?.access_token;
        if (newAccess) setAccessToken(newAccess);
        return newAccess;
    })
    .catch(err => {
        console.error("Refresh error:", err.response?.status, err.response?.data);
        throw err;
    })
    .finally(() => {
        isRefreshing = false;
        refreshPromise = null;
    });
    return refreshPromise;
}

export async function getPosts(){
    let response: Promise<any> | null = null;
    console.log("Getting posts...");
    response = await api.get("/post/",{ headers: { "Content-Type": "application/json"}, withCredentials: true })
        .then(res => {
            console.log("Get posts response:", res.data);
            return res.data;
        })
        .catch(err => {
            console.error("Get posts error:", err.response?.status, err.response?.data);
            throw err;
        });
        return response;
    
}

export async function getUserPosts(){
    let response_mes: Promise<any> | null = null;
    console.log("Getting user posts...");
    //переделать путь на нуджный
    response_mes = await api.get("/post/",{ headers: { "Content-Type": "application/json"}, withCredentials: true })
        .then(res => {
            console.log("Get posts response_mes:", res.data);
            return res.data;
        })
        .catch(err => {
            console.error("Get posts error:", err.response?.status, err.response?.data);
            throw err;
        });
        return response_mes;
    
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