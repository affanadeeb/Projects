import { useRef } from 'react';
import './App.css';
import './login.css';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Header from './Header'

let axiosConfig = {
    headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
    }
};

function Login() {
    
    const username = useRef("");
    const password = useRef("");
    const navigate = useNavigate();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        let values = {
            username: username.current.value,
            password: password.current.value
        }
        console.log(values)

        axios.post("/login", values, axiosConfig)
            .then(res => {
                if(res.data.login === 1){
                    // add session something
                    navigate(`/user/${values.username}`);
                }
                console.log(res.data.message)
            })
            .catch(err => console.log(err));
    }

    // have to add a navbar component
    return (
        <div className='App'>
            <header>
                <div className="logo">
                <i className="fa-brands fa-react"></i>
                seddit
                </div>
            </header>
            <div className='login-div'>
                <h2>Login</h2>
                <form onSubmit={handleSubmit}>
                    <label htmlFor='username'>Username</label>
                    <input ref={username} type='text' name='username' placeholder='Enter your username' className='text-input' required></input>
                    <label htmlFor='password'>Password</label>
                    <input ref={password} type='password' name='password' placeholder='enter your password' className='text-input' required></input>

                    <button type='submit'>
                        <i className="fa-solid fa-right-to-bracket login-sym"></i>
                        <span className='login-btn-text'>Login</span>
                    </button>
                    <div className='sign-up-hook'>Don't have an account? Create one <a href='/sign-up'>here.</a></div>
                </form>
            </div>
        </div>
    );
}

export default Login;
