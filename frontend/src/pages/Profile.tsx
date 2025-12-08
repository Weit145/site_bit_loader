import './Profile.css'
import Header from "../components/Header";
// import Button from "../components/button_handler";
// import { Link } from "react-router-dom";
// import type React from "react";

import { getPosts } from "../api";
import { useState, useEffect } from 'react';
import "./Pages.css"
import "../App.css"

export default function Profile (){
    const count_of_simvols=30
    const [messages, setMessages] = useState<Array<{title:string, body:string, name_img:string, user_name:string, id:number}>>([]);
    const [expandedPosts, setExpandedPosts] = useState<Set<number>>(new Set());
    
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
              setMessages(data);
            }
          })
          .catch((error) => {
            console.error("Error fetching posts:", error);
          });
      }, []); {
                console.error("Refresh failed during response handling:");
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
                            <span className="profile_text">Имя пользователя: {"Mifugi1212"}</span>
                        </div>
                        <div className='column_space'/>
                        <div className='column_user_posts' >
                            {messages.map((post, index) => {
                                // style={{backgroundColor: "rgba(0, 0, 0, 0.75)"}}
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