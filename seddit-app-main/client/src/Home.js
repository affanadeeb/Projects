import { useEffect, useState } from "react";
import "./App.css"
import { useLocation } from "react-router-dom";
import axios from "axios";
import Header from "./Header";
import PostsComponent from "./PostsComponent";
import RecommenedComponent from "./RecommendedUsers";


function Home(){
    const [name, setName] = useState("")
    const [login, setLogin] = useState(false);

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
              // navigate("/login");
            }
          })
    }, [])

    return (
        <div className="App">
            <Header login={login} self={false} username={name} />
            <RecommenedComponent />
            <PostsComponent
                self={false}
                username={name}
                user={false}
            />

        </div>
    )
}

export default Home;