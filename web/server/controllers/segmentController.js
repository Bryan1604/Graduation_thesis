const connection = require("../database/connectDB_CDP");
const moment = require('moment');

const segmentController = {
  getALL: async (req, res) => {
    try {
      const [rows, fields] = await connection.promise().query("SELECT segments.segment_id, segments.segment_name, segments.create_time, segments.update_time, COUNT(customer_segment.customer_id) AS customer_count FROM segments LEFT JOIN customer_segment ON segments.segment_id = customer_segment.segment_id GROUP BY segments.segment_id, segments.segment_name;");
      res.json({
        data: rows,
      });
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
  getById: async (req, res) => {
    try {
      const { id } = req.params;
      const [rows, fields] = await connection.promise().query("select * from segments where segment_id = ?", [id]);
      res.json({
        data: rows,
      });
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
  create: async (req, res) => {
    const create_time = moment().format('YYYY-MM-DD HH:mm:ss')
    const update_time = create_time
    try {
      const { segment_name, rule } = req.body;
      const insertSql = "INSERT INTO segments (segment_name, rule, create_time, update_time) VALUES (?, ?, ?, ?)";
      const [rows, fields] = await connection.promise().query(insertSql, [segment_name, rule, create_time, update_time]);

      res.json({
        data: rows,
      });
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
  delete: async (req, res) => {
    try {
      const { id } = req.params;
      const [rows, fields] = await connection.promise().query("delete from segments where segment_id = ?", [id]);
      res.json({
        data: rows,
      });
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
};

module.exports = segmentController;
