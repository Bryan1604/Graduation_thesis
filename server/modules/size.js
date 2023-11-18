const connection = require("../database/connectDB");

connection.connect((err) => {
    if (err) throw err;
    console.log("Connected!");
    var sql = "CREATE TABLE IF NOT EXISTS size (sizeId INT PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255))";
    connection.query(sql, function (err, result) {
        if (err) throw err;
        console.log("Table size created");
    });
});