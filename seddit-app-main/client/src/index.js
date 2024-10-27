import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import '@fortawesome/fontawesome-free/css/all.min.css';

import './index.css';
import App from './App';
import Login from './Login';
import SignUp from './SignUp';
import NewPost from './NewPost';
import Home from './Home';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/home" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/sign-up" element={<SignUp />} />
        <Route path="/new-post" element={<NewPost />} />
        <Route path="/user/:username" element={<App />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>
);