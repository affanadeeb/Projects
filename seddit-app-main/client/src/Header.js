import axios from "axios";
import { useNavigate } from "react-router-dom";

function Header({login, self, username}){
    const navigate = useNavigate();

    const handleLogout = () => {
        axios
          .get("/logout")
          .then((res) => navigate("/login"))
          .catch((err) => console.log(err));
      };

    const handleSelf = () => {
        navigate(`/user/${username}`)
    }

    const handleHome = () => {
        navigate("/home")
    }

    return (
        <header>
            <div className="logo" onClick={handleHome}>
            <i className="fa-brands fa-react"></i>
            seddit
            </div>

            <div className="search-div">
                <input className="search-box" type="text" placeholder="Search posts" />
                <i className="fa-solid fa-magnifying-glass"></i>
            </div>
            <nav className="nav-bar">
                {/* {addNewBtn ? ( */}
                    <i className="header-icon fa-solid fa-plus"></i>
                {/* ): <></>}  */}
                <i className="header-icon fa-solid fa-envelope"></i>
                <i className="header-icon fa-solid fa-bell"></i>
                <i className="header-icon fa-solid fa-globe"></i>                
                <div className="header-premium">
                    <i className="fa-solid fa-fire-flame-curved"></i>
                    <span className="header-premium-text">Premium</span>
                </div>
            </nav>

            {/*  Login status button */}
            {login ? (
                self ? (
                    <button className="logout-btn" onClick={handleLogout}>Logout</button>
                ) : 
                (
                    <button className="logout-btn" onClick={handleSelf}>Logged in as <b>{username}</b></button>
                )
            ) 
            : (
                <button className="logout-btn" onClick={handleLogout}>Login</button>   
            )}
            
        </header>
    )
}

export default Header;
