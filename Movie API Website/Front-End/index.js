const express = require("express");
const app = express();

// read all html & css files from public directory
app.use(express.static('public'))

app.get("/", (req, res) => {
  res.sendFile("/public/index.html", { root: __dirname });
});

app.get("/login/", (req, res) => {
    res.sendFile("/public/login.html", { root: __dirname });
});

app.get("/movie/", (req, res) => {
    res.sendFile("/public/movies.html", { root: __dirname });
});

app.get("/movie/:id/", (req, res) => {
    res.sendFile("/public/moviedetails.html", { root: __dirname });
});

app.get("/search-movie/:searchInput/:searchgroup/", (req, res) => {
  res.sendFile("/public/searched.html", { root: __dirname });
});

app.get("/genre/", (req, res) => {
  res.sendFile("/public/genres.html", { root: __dirname });
});


const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Client server has started listening on port ${PORT}`);
});
