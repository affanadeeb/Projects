import { useEffect, useState } from "react";
import Post from "./Post";
import axios from "axios";
import { useLoaderData, useLocation, useNavigate } from "react-router-dom";
import { getTimeDifference } from "./TimeDiff";

function PostsComponent({self, username, user}){
    const [posts, setPosts] = useState([]);
    const navigate = useNavigate();
    const location = useLocation();
    const route = user ? "/user-posts": "/all-posts"

    const handlePostsData = (res) => {
        if(!res.data.invalid_username){
          setPosts(res.data.userPosts)
        }
        else{
          console.log("User Not Found!");
        }
    }

    useEffect(() => {
        axios
            .post(route, {username: username})
            .then((res) => { handlePostsData(res)})
            .catch(err => console.log(err));
    }, [location.pathname])
    
    const handleNewPost = () => {
        navigate("/new-post")
    }

    return (
        <div className="your-posts">
            <div className="head">
                <div className="head-text">
                {user ? (
                    <><b>{username}</b>'s Posts</>
                ) : <><b>Infinite</b> Scroll</>}
                </div>
                
                {self || !user ? (
                    <div className="new-post" onClick={handleNewPost}><i className="new-post-plus fa-solid fa-plus"></i><span className="new-post-text">New Post</span></div>
                ): <></>}
            </div>
        
            {posts.map((post) => (
            <Post
                title={post.title}
                timestamp={getTimeDifference(post.time)}
                desc={post.desc}
                username={post.username}
                id={post.id}
                self={self}
            />
            ))}

      </div>
    )
}

export default PostsComponent;