import api from '../api';
import './Profile.css'
import Header from "../components/Header";
import Button from "../components/button_handler";
// import { Link } from "react-router-dom";
// import type React from "react";

import { getPosts } from "../api";
import { useState, useEffect } from 'react';
import "./Pages.css"
import "../App.css"
import type { AxiosError } from 'axios';

export default function Profile (){
    const [formFlag, setFormFlag] = useState<boolean>(false)
    
    const [username, setUsername] = useState<string>("")
    const [flag_username_error, setFlag_username_error] = useState<boolean>(false);
    const [touchedUserName, setTouchedUserName] = useState<boolean>(false);

    const [sendStatus, setSendStatus] = useState<'none'|'success'|'error'>('none');
    const [serverMessage, setServerMessage] = useState<string>('');
    const count_of_simvols=30
    const [messages, setMessages] = useState<Array<{title:string, body:string, name_img:string, user_name:string, id:number}>>([]);
    const [expandedPosts, setExpandedPosts] = useState<Set<number>>(new Set());
    function ButtonProfile(){
        setFormFlag(!formFlag)
    }
    const validateUserName = (v: string) => v.trim().length >= 4;

    function handleUserNameChange(v: string) {
        setUsername(v);
        if (touchedUserName) setFlag_username_error(!validateUserName(v));
    }

    function handleUserNameBlur() {
        setTouchedUserName(true);
        setFlag_username_error(!validateUserName(username));
    }
    function handleBlur() {
    if (handleUserNameBlur) handleUserNameBlur();
    }

    function handleChange(event: React.ChangeEvent<HTMLInputElement>){
        handleUserNameChange(event.target.value)
    }
    const togglePost = (id: number) => {
        setExpandedPosts(prev => {
            const newSet = new Set(prev);
            if (newSet.has(id)) {
                newSet.delete(id);
            } else {
                newSet.add(id);
            }
            return newSet;
        });
    };

    const isExpanded = (id: number) => expandedPosts.has(id);

      useEffect(() => {
        let mounted = true;
    
          getPosts()
          .then((data) => {
            if (mounted && Array.isArray(data)) {
              setMessages(data);onBlur
            }
          })
          .catch((error) => {
            console.error("Error fetching posts:", error);
          });
      }, []); {
                console.error("Refresh failed during response handling:");
            }


    async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
            //Используется на случай если бек принимает данные в формате application/x-www-form-urlencoded
            const params = new URLSearchParams({
            username : username,
            })
            try {
            const response = await api.post(
            //Изменить путь
            "/post/",
            { username: username},
            { headers: { "Content-Type": "application/json" } }
            );
            setSendStatus('success');
        } catch (error: any) {
            setSendStatus('error');
            const serverMessage = error.response?.data?.details
            ? Array.isArray(error.response.data.details)
                ? error.response.data.details.join('\n')
                : String(error.response.data.details)
            : error.response?.data?.message || error.message || 'Ошибка при отправке';
            setServerMessage(serverMessage);
            console.error("Ошибка при отправке данных:", error.response?.data || error.message);
        }
    }
    return(
        <div>
            <Header />
            <main>
                <div className = "content_box">
                    <div className="profile_lable_text">Профиль</div>
                    <div className='test_row'>
                        <div className='column_profile_info'>
                            <span className="profile_text"><img src="../../public/default.png" alt="Default_photo" className="image_profile"/></span>
                            <span className="profile_text">Ник: <span style={{color:"red"}}>@{"fugi"}</span></span>
                            <span className="profile_text">Имя пользователя: {!formFlag && "Mifugi1212"}</span>
                            {formFlag &&
                                <form>
                                    <input type="text"
                                            style={{maxWidth:"100%"}}
                                            onChange={handleChange}
                                            onBlur={handleBlur} 
                                            className={flag_username_error==true ? "input_area_incorrect" : "input_area" }/>
                                    <Button 
                                    type="submit"
                                    flag_disabled={username.length<=3 || flag_username_error}
                                    onClick={null}
                                    style={{position:"relative", marginRight:"10vw"}}
                                    >Подтвердить</Button>
                                </form>}
                            <Button 
                            type="button"
                            flag_disabled={false}
                            onClick={()=>ButtonProfile()}
                            >{!formFlag ? "Редактировать" : "Отмена"}</Button>

                        </div>
                        <div className='column_space'/>
                        <div className='column_user_posts' >
                            {messages.map((post, index) => {
                                const truncated = post.body.length > count_of_simvols;
                                const shouldShowFull = isExpanded(post.id);
                                const displayText = shouldShowFull || !truncated
                                    ? post.body
                                    : post.body.slice(0, count_of_simvols - 3) + "...";
                                return(
                                <button key={post.id}
                                        onClick={() => togglePost(post.id)}
                                        style={{ border: 'none', background: 'none', cursor: 'pointer'}}>
                                    <div className="content_text" key={index} >
                                        <div className="lable_text">{post.title}</div>
                                        <span style={{color:"red"}}>  {post.user_name + "@kload" }</span>
                                        <span>:</span>
                                        <span style={{color: "green"}}>~</span>
                                        <span>$ </span>
                                        {displayText}
                                    </div>
                                </button>
                                )
                            })}
                        </div>
                    </div>
                </div>
            </main>
        </div>
    )
}