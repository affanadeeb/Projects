const bodyParser = require("body-parser");
const path = require('path');
const cookieParser = require("cookie-parser");
const express = require("express");
const multer = require('multer');
const session = require("express-session");
const fs = require("fs");
const os = require("os")
const { pid } = require("process");

const app = express();
app.use('/images', express.static(path.join(__dirname, 'images')));
app.use(bodyParser.json({ limit: '8mb' }));
app.use(cookieParser());
app.use(express.urlencoded({ extended: true }));
app.use(
  session({
    secret: "secret",
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: false,
      maxAge: 1000 * 60 * 60 * 24,
    },
  })
);

// for storing images
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'images/'); 
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname).toLowerCase();

    // Check if the file is a PNG image
    if (ext !== '.png') {
      const error = new Error('Only PNG files are allowed');
      error.code = 'FILE_TYPE';
      return cb(error);
    }

    cb(null, req.body.name + '-' + "default" + path.extname(file.originalname));
  },
});

const upload = multer({ storage: storage });
  
const PORT = 4000;
const numberOfPostsToShow = 10; // Change this value to the desired number

const usersDB = "users.json";
const postsDB = "posts.json";
let usersArray = [];
let postsArray = [];

const updatePostsFile = () => {

  const jsonPosts = JSON.stringify(postsArray, null, 2);
  fs.writeFileSync(postsDB, jsonPosts, "utf-8");

}
const handleServerClose = () => {
  // Save data to the file before closing the server
  const jsonData = JSON.stringify(usersArray, null, 2);

  fs.writeFileSync(usersDB, jsonData, "utf-8");
};

const getTimestamp = () => {
  return new Date().getTime();
}

try {
  const fileContent = fs.readFileSync(usersDB, "utf-8");
  usersArray = JSON.parse(fileContent);

  const postsContent = fs.readFileSync(postsDB, "utf-8");
  postsArray = JSON.parse(postsContent);

} catch (error) {
  console.error(
    "Error reading or parsing one of the JSON file:",
    error.message
  );
}

const renameFile = (defaultImagePath, newImagePath) => {
  if (fs.existsSync(defaultImagePath)) {
    fs.rename(defaultImagePath, newImagePath, (err) => {
      if (err) {
        console.error("Error renaming file:", err);
      } else {
        // console.log("File renamed successfully!");
      }
    });
  } else {
    console.log("Default image file does not exist.");
  }
}

app.post("/new-post", upload.single("image"), (req, res) => {
  let title = req.body.title
  let desc = req.body.desc
  let username = req.body.name
  let timestamp = getTimestamp()

  if(req.session.username != username){
    res.send("Be civilized, MF!");
    return
  }

  renameFile(path.join("images", `${username}-default.png`), path.join("images", `${username}-${timestamp}.png`));    
  
  postsArray.unshift({
    title: title,
    desc: desc,
    time: timestamp,
    username: username,
    id: `${username}-${timestamp}`
  })

  updatePostsFile();
  res.send("Success")
})

app.post("/delete-post", (req, res) => {
  let postId = req.body.id
  let username = postId.split("-")[0];

  if(req.session.username != username){
    res.send({message: "Be civilized, MF!"});
    return
  }

  postsArray = postsArray.filter(obj => obj.id !== postId);
  updatePostsFile()
  res.send({message: "Deletion Success!"})
})

app.post("/all-posts", (req, res) => {
  let username = req.body.username;

  const num = postsArray.length < numberOfPostsToShow ? postsArray.length : numberOfPostsToShow;
  const selectedPosts = postsArray.slice(0, num);
  
  const jsonObject = {
    invalid_username: false,
    userPosts: selectedPosts
  }

  res.json(jsonObject)
})

app.post("/user-posts", (req, res) => {
  let userPosts = [];
  const username = req.body.username;
  // console.log(username)

  postsArray.forEach(el => {
    if(el.username == username)
      userPosts.push(el)
  })

  const jsonObject = {
    invalid_username: checkUsername(username),
    userPosts: userPosts
  }

  // console.log(userPosts)
  res.json(jsonObject);
})

app.get("/", (req, res) => {
  res.send("Test Server!");
});

app.get("/verify-login", (req, res) => {
  if (req.session.username) {
    res.json({ valid: true, username: req.session.username });
  } else {
    res.json({ valid: false });
  }
});

const getRandomItems = (array, n) => {
  if (array.length <= n) 
    return array.slice(); 

  const shuffledArray = array.sort(() => Math.random() - 0.5);
  return shuffledArray.slice(0, n);
};


app.get("/suggested-users", (req, res) => {

  // have to serve according to req.session.username 
  // for now, returning 5 random users
  const suggestedUsers = getRandomItems(usersArray, 5).map(el => ({username: el.username}));

  res.json({message: "Success!", usersArray: suggestedUsers});
})

app.post("/login", (req, res) => {
  let username = req.body.username;
  let password = req.body.password;

  let response = {
    login: 0,
    message: "Entry Not Found for such user!",
  };
  usersArray.forEach((el) => {
    if (el.username == username) {
      response.login = -1;
      response.message = "Password is Incorrect!";
      if (el.password == password) {
        response.login = 1;
        response.message = "Logged In!";
        req.session.username = el.username;
      }
    }
  });
  res.json(response);
});

const checkUsername = (username) => {
  return !usersArray.some(el => el.username === username);
}

app.post("/sign-up", (req, res) => {
  let username = req.body.username;
  let password = req.body.password;
  let email = req.body.email;

  if(checkUsername(username) == false){
    res.json({ message: "Username exists!!", signUp: 0 })
    return
  }

  usersArray.push({ username: username, password: password, email: email });
  handleServerClose();

  // console.log(usersArray);
  res.json({ message: "Sign Up Successful!", signUp: 1 });
});

app.get("/logout", (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      console.error(err);
      return res.sendStatus(500);
    }
    res.send("Logged out successfully!");
  });
});

process.on("exit", handleServerClose);

app.listen(PORT, () => {
  console.log(`Server running on PORT ${PORT}`);
});
