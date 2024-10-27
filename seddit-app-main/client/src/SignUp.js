import { useRef } from 'react';
import './login.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

let axiosConfig = {
    headers: {
        'Content-Type': 'application/json;charset=UTF-8',
        "Access-Control-Allow-Origin": "*",
    }
};

function SignUp() {
    
    const username = useRef("");
    const password = useRef("");
    const email = useRef("");

    const navigate = useNavigate();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        let val_username = username.current.value
        let val_password = password.current.value
        let val_email = email.current.value
        let values = {
            username: val_username,
            password: val_password,
            email: val_email
        }
        console.log(values)
        
        axios.post("/sign-up", values, axiosConfig)
            .then(res => {
                if(res.data.signUp){
                    navigate("/login")
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
                <h2>Sign Up</h2>
                <form onSubmit={handleSubmit}>
                    <label htmlFor='username'>Username</label>
                    <input ref={username} type='text' name='username' placeholder='enter your Username' className='text-input' required></input>
                    <label htmlFor='email'>Email:</label>
                    <input ref={email} type='email' name='email' placeholder='enter your Email' className='text-input'required></input>
                    <label htmlFor='password'>Password</label>
                    <input ref={password} type='password' name='password' placeholder='enter your Password' className='text-input'required></input>

                    <button type='submit'>
                        <i className="fa-solid fa-user-plus login-sym"></i>
                        <span className='login-btn-text'>SignUp</span>
                    </button>
                    <div className='sign-up-hook'>Already have an account? Login <a href='/login'>here.</a></div>
                </form>
            </div>
        </div>
    );
}

export default SignUp;
