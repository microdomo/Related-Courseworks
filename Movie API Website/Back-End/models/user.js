// Class: DISM/FT/2B/21
// Admission Number: p2026073
// Name: Tan Ying Xuan Shermaine

var db = require('./databaseConfig.js');

var userDB = {
    // ==============================================
    //                     Login
    // ==============================================
    login: function (username, password, callback) {

        var dbConn = db.getConnection();
        dbConn.connect(function (err) {
    
          if (err) {//database connection gt issue!
            console.log(err);
            return callback(err, null);
          } 
          else {
            const query = "SELECT * FROM user WHERE username=? AND password=?";
    
            dbConn.query(query, [username, password], (error, results) => {
                dbConn.end();
                if (error) {
                    callback(error, null);
                    return;
                }
                if (results.length === 0) {
                    return callback(null, null);
        
                } else {                    
                    const user = results[0];
                    return callback(null, user);
                }
            });
          }
        });
    },
    // ==============================================
    //                     Verify
    // ==============================================
    verifyUser: function (userid, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err, null, null);
            }
            else {
                console.log("Connected!");

                var sql = 'SELECT userid,username,type FROM user WHERE userid = ?';

                conn.query(sql, [userid], function (err, result) {
                    conn.end();

                    if (err) {
                        console.log(err);
                        return callback(err, null);
                    }
                    if (result.length == 0) {
                        return callback(null, null)
                    }
                    else {
                        return callback(null, result)
                    }
                });
            }
        })
    },
    // ==============================================
    //                   Endpoint 1
    // ==============================================
    addUser: function (username, email, contact, password, type, profile_pic_url, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var addUserQuery = 'INSERT INTO user(username, email, contact, password, type, profile_pic_url) VALUES(?,?,?,?,?,?);';

                conn.query(addUserQuery, [username, email, contact, password, type, profile_pic_url], function (err, result) {
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
    //                   Endpoint 2
    // ==============================================
    getUsers: function (callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getUsersQuery = 'SELECT userid, username, email, contact, type, profile_pic_url FROM user';
                conn.query(getUsersQuery, [], function (err, result) {
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
    //                   Endpoint 3
    // ==============================================
    getUserbyID: function (id, callback) {
        var conn = db.getConnection();
        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err,null);
            }
            else {
                console.log("Connected!");
                var getUserbyIDQuery = 'SELECT userid, username, email, contact, type, profile_pic_url FROM user WHERE userid = ?';
                conn.query(getUserbyIDQuery, [id], function (err, result) {
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
    //                   Endpoint 4
    // ==============================================
    editUser: function(username, email, contact, password, type, profile_pic_url, id, callback) {
        var conn = db.getConnection();

        conn.connect(function (err) {
            if (err) {
                console.log(err);
                return callback(err, null);
            }
            else {
                console.log("Connected!");
                var editUserQuery = `UPDATE user SET username = ?, email = ?, contact = ?, password = ?, type = ?, profile_pic_url = ? WHERE userid = ?`;
                conn.query(editUserQuery, [username, email, contact, password, type, profile_pic_url, id], function (err, result) {
                    conn.end();
                    if (err) {
                        console.log(err)
                        return callback(err,null);
                    };
                    return callback(null,result);
                });
            }
        });
    }
}

module.exports = userDB