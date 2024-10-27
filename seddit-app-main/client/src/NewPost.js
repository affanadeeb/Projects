import { useEffect, useRef, useState } from "react";
import "./App.css"
import Header from "./Header";
import { useNavigate } from "react-router-dom";
import axios from "axios";

let axiosConfig = {
    headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
    }
};

function NewPost(){
    const [name, setName] = useState("");
    const [login, setLogin] = useState(false);
    const [selectedImage, setSelectedImage] = useState(null);

    const navigate = useNavigate();
    const titleRef = useRef();
    const descRef = useRef();
    const fileRef = useRef();

    useEffect(() => {
      axios
        .get("/verify-login")
        .then((res) => {
          if (res.data.valid) {
            setName(res.data.username);
            setLogin(true);
            console.log("Verified!");
          } else {
            console.log("No login found!");
            navigate("/login");
          }
        })
      }, []);

    const handleCreatePost = (event) => {
        event.preventDefault()

        const formData = new FormData();
        formData.append("title", titleRef.current.value)
        formData.append("desc", descRef.current.value)
        formData.append("name", name)
        formData.append("image", selectedImage); 

        axios
            .post("/new-post", formData, {
              headers: {
                "Content-Type": "multipart/form-data"
              }
            })
            .then(res => navigate(`/user/${name}`))
            .catch(err => console.log(err));
    }

    const handleFileInput = (event) => {
      let file = event.target.files[0];
    
      if(file){
        fileRef.current.innerText = file.name
        setSelectedImage(file);
      }
    }

    return (
        <div className="App">
            <Header 
              login={login}
              self={1}
              username={name} 
            />
            <form className="new-post-container" onSubmit={handleCreatePost}>
                <div className="new-post-cont-head">New Post</div>
                
                <input className="input-post-title" ref={titleRef} type="text" placeholder="title of the post" required/>
                
                <textarea className="textarea-post-desc" ref={descRef} placeholder="some description for the post"></textarea>
                
                <label ref={fileRef} htmlFor="picture" className="input-post-image"><i className="fa-solid fa-cloud"></i>Choose Image</label>
                <input type="file" id="picture" accept="image/png" onChange={handleFileInput} name="image" hidden/>
                
                <div className="post-by">Post by: <u><b>{name}</b></u></div>
                <button className="post-btn" type="submit">
                  <i className="fa-solid fa-paper-plane"></i>
                  <span className="post-btn-text">Post</span>
                </button>
            
            </form>
        </div>
    )
}

export default NewPost;