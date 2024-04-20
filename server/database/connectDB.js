require("dotenv").config()

// get the client
const mysql = require("mysql2");

const dbHost = process.env.DB_HOST || "localhost";
// create the connection to database
const connection = mysql.createConnection({
  host: dbHost,
  user: "root",
  password: process.env.DB_PASSWORD,
  database: "CDP",
  multipleStatements: true,
});

connection.connect();

module.exports = connection;
