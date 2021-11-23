// Class: DISM/FT/2B/21
// Admission Number: p2026073
// Name: Tan Ying Xuan Shermaine

var db = require('./databaseConfig.js');

var movieDB = {
    // ==============================================
    //                   Endpoint 7
    // ==============================================
    addMovie: function (title, description, cast, genreid, time, openingdate, image, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var addMovieQuery = 'INSERT INTO movietable(title, description, cast, time, \`opening date`\, image) VALUES(?,?,?,?,?,default);';
                var addMovieGenreQuery = 'INSERT INTO moviegenre(moviewithgenreid, genreid, genre) VALUES(?,?, (SELECT genre FROM genretable WHERE genreid = ?));';

                conn.query(addMovieQuery, [title, description, cast, time, openingdate, image], function (err, movie) {
                    if (err) {
                        return callback(err,null);
                    } 
                    else {
                        var splitgenres = genreid.split(",");
                        for (i = 0; i < splitgenres.length; i++){
                            genreid = splitgenres[i];
                            conn.query(addMovieGenreQuery, [movie.insertId, genreid, genreid], function (err, result) {
                                if (err) {
                                    return callback(err,null);
                                }
                            });
                            if (i == splitgenres.length) {
                                conn.end();
                                break;
                            }
                        }
                        return callback(null, movie.insertId);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Endpoint 8
    // ==============================================
    getMovies: function (callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getMoviesQuery = 'SELECT * FROM movietable';
                conn.query(getMoviesQuery, [], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        console.log(result)
                        return callback(null, result);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Search Movies
    // ==============================================
    searchMovies: function(searchInput, searchgroup, callback ) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var searchMoviesQuery = 'SELECT movieid, image, title, time ';
                
                if (searchInput == "empty") {
                    searchMoviesQuery += ""
                }
                else {
                    if (searchgroup == "title") {
                        searchInput = '%' + searchInput + '%'
                        searchMoviesQuery += " FROM movietable WHERE title LIKE " + "'" + searchInput + "'"
                    }
                    else if (searchgroup == "genre"){
                        searchInput = '%' + searchInput + '%'
                        searchMoviesQuery += " , genre FROM movietable JOIN moviegenre ON movieid = moviewithgenreid WHERE genre LIKE " + "'" + searchInput + "'"
                    }
                }

                console.log(searchMoviesQuery)
                conn.query(searchMoviesQuery, [], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        for (var i = 0; i < result.length; i++) {
                            for (var n = i + 1; n < result.length; n++) {
                                if (result[i].movieid == result[n].movieid) {
                                    delete(result[i])
                                }
                                result = result.filter(function(element) {
                                    return element !== undefined;
                                });
                            }
                        }
                        return callback(null, result);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Endpoint 9
    // ==============================================
    getMoviesbyID: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getMoviesQuery = 'SELECT image, image2, title,description,cast,time,\`opening date`\ ,GROUP_CONCAT(genre) genres FROM movietable JOIN moviegenre ON movieid = moviewithgenreid WHERE movieid = ?';
                
                conn.query(getMoviesQuery, [id], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        return callback(null, result);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Endpoint 10
    // ==============================================
    deleteMovie: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var deleteMovieQuery = 'DELETE FROM movietable WHERE movieid = ?';
                
                conn.query(deleteMovieQuery, [id], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        return callback(null, result);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Endpoint 11
    // ==============================================
    addReview: function (movieid, userid, rating, review, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var addUserQuery = 'INSERT INTO reviewtable(movieid, userid, rating, review) VALUES(?,?,?,?);';

                conn.query(addUserQuery, [movieid, userid, rating, review], function (err, result) {
                    conn.end();
                    if (err) {
                        return callback(err,null);
                    } else {
                        return callback(null,result.insertId);
                    }
                });
            }
        });
    },
    // ==============================================
    //                   Endpoint 12
    // ==============================================
    getReviewsOfMovie: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getReviewsQuery = 'SELECT movieid, reviewtable.userid, user.username, rating, review, reviewtable.created_at FROM reviewtable LEFT JOIN user ON reviewtable.userid = user.userid WHERE movieid = ?';
                
                conn.query(getReviewsQuery, [id], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        console.log(result)
                        return callback(null, result);
                    }
                });
            }
        });
    },
    // ==============================================
    //                 Average Ratings
    // ==============================================
    getAverageRating: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getReviewsQuery = 'SELECT AVG(rating) AS rating FROM reviewtable WHERE movieid = ?';
                
                conn.query(getReviewsQuery, [id], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err);
                        return callback(err,null);
                    } else {
                        return callback(null, result);
                    }
                });
            }
        });
    },
}

module.exports = movieDB