import "./App.css";
import { useLocation, useNavigate, useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./Header";
import PostsComponent from "./PostsComponent";

function App() {
  const { username } = useParams();
  const [name, setName] = useState("");
  const [login, setLogin] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get("/verify-login").then((res) => {
      if (res.data.valid) {
        setName(res.data.username);
        setLogin(true);
        console.log("Verified!");
      } else {
        console.log("No login found!");
        // navigate("/login");
      }
    });
  }, []);

  return (
    <div className="App">
      
      <Header 
        login={login} 
        self={name === username} 
        username={name} 
      />
      
      <PostsComponent
        self={name === username}
        username={username}
        user={true}
      />

    </div>
  );
}

export default App;
