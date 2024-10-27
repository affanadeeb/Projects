import { useEffect, useState } from "react";
import "./App.css"
import axios from "axios";
import { useNavigate } from "react-router-dom";

function SuggestedUser({name}){
    const navigate = useNavigate()

    const handleUser = (username) => {
        navigate(`/user/${username}`)
    }
    
    return (
        <div className="rec-user-div" onClick={() => handleUser(name)}>
            <div className="rec-user-dp"></div>
            <div className="rec-user-name">{name}</div>
        </div>
    )
}

function RecommenedComponent(){
    const [users, setUsers] = useState([]);

    useEffect(() => {
        axios
            .get("/suggested-users")
            .then(res => {
                setUsers(res.data.usersArray)
            })
            .catch(err => console.log(err));
    }, [])

    return (
        <div className="rec-users">
            <div className="rec-user-head">Suggested for You</div>
            <div className="rec-users-container">
                {users.map((el) => (
                    <SuggestedUser name={el.username} />
                ))}
            </div>
        </div>
    )
}
export default RecommenedComponent;