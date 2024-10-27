import axios from "axios";
import "./App.css"
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

function Post({title, timestamp, desc, username, id, self}){
    const postRef = useRef();
    const [imageExists, setImageExists] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        axios
        .get(`/images/${id}.png`)
        .then(res => {
            if(res.status == 404){    
                setImageExists(false)
            }
            else
                setImageExists(true)
        })
        .catch(err => console.log(err));
    }, [])

    const handleDeletePost = (pid) => {
        axios
            .post("/delete-post", {id: pid})
            .then(res => {
                console.log(res.data.message)
                postRef.current.style.opacity = 0
                setTimeout(() => {
                    postRef.current.style.display = "none"
                }, 400);
            })
            .catch(err => console.log(err))
    }

    const handleUserPage = (username) => {
        navigate(`/user/${username}`)
    }

    return (
        <div ref={postRef} className="post" id={id}>
            <div className="post-left">
                <div className="post-head">{title}</div>
                <pre className="post-desc">{desc}</pre>
                <div>
                    <div className="post-user" onClick={() => handleUserPage(username)}><i className="fa-solid fa-circle-user"></i>{username}</div>
                    <div className="post-time"><i className="fa-solid fa-clock"></i>{timestamp}</div>
                </div>
                {self ? (
                    <div className="post-delete" onClick={() => handleDeletePost(id)}><i className="fa-regular fa-trash-can"></i></div>
                ): <></>}
            </div>
            {imageExists ? 
            (
                <img className="post-img" src={"../images/" + id + ".png"}/>
            ) : <></>}
        </div>
    )
}

export default Post;