// Class: DISM/FT/2B/21
// Admission Number: p2026073
// Name: Tan Ying Xuan Shermaine

var mysql = require('mysql');
var dbconnect = {
    getConnection: function () {
        var conn = mysql.createConnection({
            host: "localhost",
            user: "root",
            password: "root",
            database: "sp_movies",
            dateStrings: true
        });     
        return conn;
    }
};

module.exports = dbconnect