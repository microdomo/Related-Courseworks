// Class: DISM/FT/2B/21
// Admission Number: p2026073
// Name: Tan Ying Xuan Shermaine

var db = require('./databaseConfig.js');

var genreDB = {
    // ==============================================
    //                   Endpoint 5
    // ==============================================
    addGenre: function (genre, description, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var addGenreQuery = 'INSERT INTO genretable(genre, description) VALUES(?,?);';

                conn.query(addGenreQuery, [genre, description], function (err, result) {
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
    //                   Endpoint 6
    // ==============================================
    getGenres: function (callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getGenreQuery = 'SELECT * FROM genretable';
                conn.query(getGenreQuery, [], function (err, result) {
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
    //                 Search by genre ID
    // ==============================================
    searchGenres: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");

                var MatchWithMovieQuery = 'SELECT image, movieid, title, time, genre FROM movietable JOIN moviegenre ON moviewithgenreid = movieid WHERE genreid = ?'
                
                conn.query(MatchWithMovieQuery, [id], function (err, result) {
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
    }
}

module.exports = genreDB