// Class: DISM/FT/2B/21
// Admission Number: p2026073
// Name: Tan Ying Xuan Shermaine

var express = require("express");
var app = express();

var user = require("../models/user.js");
var genreDB= require('../models/genre.js');
var movieDB = require('../models/movie.js');
// var verifyToken = require('../auth/verifyToken.js');
const isLoggedInMiddleware = require("../auth/isLoggedInMiddleware.js");


var bodyParser=require('body-parser');
var urlencodedParser=bodyParser.urlencoded({extended:false});

app.use(bodyParser.json());
app.use(urlencodedParser);

const cors = require("cors");
app.use(cors());


const jwt = require("jsonwebtoken");
const JWT_SECRET = require("../config.js"); 
// ==============================================
//                     Login
// ==============================================
app.post("/login/", (req, res) => {
    user.login(
      req.body.username,
      req.body.password,
      (error, user) => {
        if (error) {
          res.status(500).send("Wrong password or username!");
          return;
        }
        if (user === null) {
          res.status(401).send("Wrong password or username!");
          return;
        }
        const payload = { user_id: user.userid };
        jwt.sign(payload, JWT_SECRET.key, { algorithm: "HS256" }, (error, token) => {
          if (error) {
            console.log(error);
            res.status(401).send();
            return;
          }
          var userInfo = {
            "userid": user.userid,
            "username": user.username,
            "email": user.email,
            "type": user.type,
            "profile_pic_url": user.profile_pic_url
            }
          res.status(200).send({
            token: token,
            user_id: user.userid,
            loggedInAs: user.type,
            username: user.username,
            userInfo: JSON.stringify(userInfo)
          });
        })
    });
 });
// ==============================================
//                   Endpoint 1
// ==============================================
app.post('/users/',  function (req, res) {
    var username = req.body.username;
    var email = req.body.email; 
    var contact = req.body.contact;
    var password = req.body.password;
    var type = req.body.type;
    var profile_pic_url = req.body.profile_pic_url;

    user.addUser(username, email, contact, password, type, profile_pic_url, function (err, result) {
        if (!err) {
            console.log(result);
            res.status(201).send('{\n"userid": ' + result + ' \n}');
        } else{
            if(err.code == 'ER_DUP_ENTRY') {
                res.status(422).send("The new username provided already exists.");
            }
            else{
            res.status(500).send(err);
            }
        }
    });
});
// ==============================================
//                   Endpoint 2
// ==============================================
app.get("/users/", function (req,res) {
    user.getUsers (function (err,result){
        if (!err) {
            res.status(200).send(result);
        }
        else {
            res.status(500).send('{"Result":"Internal Error"}');
        }
    })
});
// ==============================================
//                   Endpoint 3
// ==============================================
app.get('/users/:id/', function (req, res) {
    var id = req.params.id;

    user.getUserbyID(id, function (err, result) {
        if (!err) {
            res.status(200).send(result);
        }else{
            res.status(500).send('{"Result":"Internal Error"}');
        }
    });
});
// ==============================================
//                   Endpoint 4
// ==============================================
app.put("/users/:id", function (req,res) {
    var id = req.params.id;
    var username = req.body.username;
    var email = req.body.email; 
    var contact = req.body.contact;
    var password = req.body.password;
    var type = req.body.type;
    var profile_pic_url = req.body.profile_pic_url;

    user.editUser(username, email, contact, password, type, profile_pic_url, id, function(err, result) {
        if (id !== req.decodedToken.user_id) {
            res.status(403).send();
        }
        else {
            if (!err) {
                res.status(204).send(result);
            }
            else {
                if(err.code == 'ER_DUP_ENTRY') {
                    res.status(422).send("The new username provided already exists.");
                }
                else{
                    res.status(500).send(err);
                }
            }
        }
    });
});
// ==============================================
//                   Endpoint 5
// ==============================================
app.post('/genre', isLoggedInMiddleware,  function (req, res) {
    const userid = parseInt(req.body.userid);
    var genre = req.body.genre;
    var description = req.body.description; 

    if (isNaN(userid)) {
        res.status(400).send();
        return;
    }
    user.verifyUser(userid, function (err, result) {
        if (err) {
            console.log(err);
            res.status(500).send();
            return;
        }
        else {
            if (result[0].type !== "Admin") {
                console.log('You do not have the rights to use this command.');
                res.status(401).send();
                return;
            }
            if (userid !== req.decodedToken.user_id) {
                res.status(403).send();
                return;
            }        
            else {
                genreDB.addGenre(genre, description, function (err, result) {
                    if (!err) {
                        console.log(result);
                        res.status(201).send('{\n"genreid": ' + result + ' \n}');
                    } 
                    else{
                        if(err.code == 'ER_DUP_ENTRY') {
                            res.status(422).send("The movie provided already exists.");
                        }
                        else {
                            res.status(500).send(err);
                        }
                    }
                });
            }
        }
    });
});
// ==============================================
//                   Endpoint 6
// ==============================================
app.get("/genre/", function (req,res) {
    genreDB.getGenres (function (err,result){
        if (!err) {
            res.status(200).send(result);
        }
        else {
            res.status(500).send('{"Result":"Internal Error"}');
        }
    })
});
// ==============================================
//                 Search by genre ID
// ==============================================
app.get("/genre/:id", function (req,res) {
    var id = req.params.id;

    genreDB.searchGenres (id, function (err,result){
        if (!err) {
            console.log(result)
            res.status(200).send(result);
        }
        else {
            res.status(500).send('{"Result":"Internal Error"}');
        }
    })
});
// ==============================================
//                   Endpoint 7
// ==============================================
app.post('/movie/', isLoggedInMiddleware,function (req, res) {
    const userid = parseInt(req.body.userid);
    var title = req.body.title;
    var description = req.body.description; 
    var cast = req.body.cast;
    var genreid = req.body.genreid;
    var time = req.body.time;
    var openingdate = req.body['opening date'];
    var image = req.body.image;

    if (isNaN(userid)) {
        res.status(400).send();
        return;
    }

    user.verifyUser(userid, function (err, result) {
        if (err) {
            console.log(err);
            res.status(500).send();
            return;
        }
        else {
            if (result[0].type !== "Admin") {
                console.log('You do not have the rights to use this command.');
                res.status(401).send();
                return;
            }
            if (userid !== req.decodedToken.user_id) {
                res.status(403).send();
                return;
            }        
            else {
                movieDB.addMovie(title, description, cast, genreid, time, openingdate, image, function (err, result) {     
                    if (!err) {
                        res.status(201).send('{\n"movieid": ' + result + ' \n}');
                    } 
                    else {
                        if(err.code == 'ER_DUP_ENTRY') {
                            res.status(422).send("The movie provided already exists.");
                        }
                        else {
                            res.status(500).send(err);
                        }
                    }
                });
            }
        }
    });
});
// ==============================================
//                   Endpoint 8
// ==============================================
app.get("/movie/", function (req,res) {
    movieDB.getMovies (function (err,result){
        if (!err) {
            res.status(200).send(result);
        }
        else {
            res.status(500).send('{"Result":"Internal Error"}');
        }
    })
});
// ==============================================
//                   Search Movies
// ==============================================
app.get("/search-movie/:searchInput/:searchgroup/", function (req,res) {
    var searchInput = req.params.searchInput;
    var searchgroup = req.params.searchgroup;

    movieDB.searchMovies (searchInput, searchgroup, function (err,result){
        if (!err) {
            res.status(200).send(result);
        }
        else {
            res.status(500).send('{"Result":"Internal Error"}');
        }
    })
});
// ==============================================
//                   Endpoint 9
// ==============================================
app.get('/movie/:id/', function (req, res) {
    var id = req.params.id;

    movieDB.getMoviesbyID(id, function (err, result) {
        if (!err) {
            res.status(200).send(result);
            console.log(result)
        }else{
            res.status(500).send('{"Result":"Internal Error"}');
        }
    });
});
// ==============================================
//                   Endpoint 10
// ==============================================
app.delete('/movie/:id/', isLoggedInMiddleware, function (req, res) {
    const userid = parseInt(req.body.userid);
    var movieid = req.params.id;

    if (isNaN(userid)) {
        res.status(400).send();
        return;
    }
    user.verifyUser(userid, function (err, result) {
        if (err) {
            console.log(err);
            res.status(500).send();
            return;
        }
        else {
            if (result[0].type !== "Admin") {
                console.log('You do not have the rights to use this command.');
                res.status(401).send();
                return;
            }
            if (userid !== req.decodedToken.user_id) {
                res.status(403).send();
                return;
            }        
            else {
                movieDB.deleteMovie(movieid, function (err, result) {
                    if (!err) {
                        res.status(204).send(result);
                    }
                    else{
                        res.status(500).send('{"Result":"Internal Error"}');
                    }
                });
            }
        }
    });
});
// ==============================================
//                   Endpoint 11
// ==============================================
app.post('/movie/:id/review/', isLoggedInMiddleware,  function (req, res) {
    const userid = parseInt(req.body.userid);
    var rating = req.body.rating; 
    var review = req.body.review;
    var movieid = req.params.id;

    if (isNaN(userid)) {
        res.status(400).send();
        return;
    }
    user.verifyUser(userid, function (err, result) {
        if (err) {
            console.log(err);
            res.status(500).send();
            return;
        }
        else {
            if (userid !== req.decodedToken.user_id) {
                res.status(403).send();
                return;
            }        
            else {
                movieDB.addReview(movieid, userid, rating, review, function (err, result) { 
                    if (err) {
                        res.status(500).send('{"Result":"Internal Error"}');
                    }
                    else {
                        res.status(201).send('{\n"reviewid": ' + result + ' \n}');
                    }
                })
            }
        }
    });
});
// ==============================================
//                   Endpoint 12
// ==============================================
app.get('/movie/:id/reviews', function (req, res) {
    var id = req.params.id;

    movieDB.getReviewsOfMovie(id, function (err, result) {
        if (!err) {
            res.status(200).send(result);
        }else{
            res.status(500).send('{"Result":"Internal Error"}');
        }
    });
});
// ==============================================
//                 Average Ratings
// ==============================================
app.get('/movie/:id/reviews/rating', function (req, res) {
    var id = req.params.id;

    movieDB.getAverageRating(id, function (err, result) {
        if (!err) {
            res.status(200).send(result);
        }else{
            res.status(500).send('{"Result":"Internal Error"}');
        }
    });
});

module.exports = app
