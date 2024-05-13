
require('dotenv').config()

// get the client
const mysql = require("mysql2");

const dbHost = process.env.DB_HOST || "localhost";
console.log(100000);
console.log(process.env['SOCKET_PATH']);
// create the connection to database

const cdp_connection = mysql.createConnection({
  host: dbHost,
  user: "root",
  password: "12345678",
  database: "CDP_DB",
  multipleStatements: true,
});
cdp_connection.connect();
module.exports =  cdp_connection ;
