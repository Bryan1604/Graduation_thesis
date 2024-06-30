const connection = require("../database/connectDB_CDP");
const moment = require('moment');
const fetch = require('node-fetch');
const segmentController = {
  getALL: async (req, res) => {
    try {
      const [rows, fields] = await connection.promise().query("SELECT segments.segment_id, segments.segment_name, segments.created_at, segments.updated_at, COUNT(customer_segment.customer_id) AS customer_count FROM segments LEFT JOIN customer_segment ON segments.segment_id = customer_segment.segment_id GROUP BY segments.segment_id, segments.segment_name;");
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
      const [segmentDetail, fields] = await connection.promise().query("select * from segments where segment_id = ?", [id]);
      const [customers, field1] = await connection.promise().query(
        "select * from customers join customer_segment on customers.customer_id = customer_segment.customer_id where customer_segment.segment_id = ? ", [id]); 
      res.json({
        segmentDetail: segmentDetail,
        customers: customers
      });
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
  create: async (req, res) => {
    try {
      const { segment_name, rule } = req.body;
      const insertSql = "INSERT INTO segments (segment_name, rule) VALUES (?, ?)";
      const [rows, fields] = await connection.promise().query(insertSql, [segment_name, rule]);
      res.json({
        data: rows,
      });
      
      // Thông tin cấu hình của Airflow
      const AIRFLOW_API_URL = 'http://localhost:8082/api/v1';
      const AIRFLOW_USERNAME = 'admin';
      const AIRFLOW_PASSWORD = 'admin';

      const DAG_ID = 'process_one_segment';
      
      try {
        // Gửi yêu cầu HTTP POST đến API của Airflow để trigger DAG
        // const fetch = await import('node-fetch').then(module => module.default);
        const response = await fetch(`${AIRFLOW_API_URL}/dags/${DAG_ID}/dagRuns`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + Buffer.from(`${AIRFLOW_USERNAME}:${AIRFLOW_PASSWORD}`).toString('base64'),
          },
          body: JSON.stringify({
            "conf": {}
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('DAG triggered successfully:', responseData);
      } catch (error) {
        console.error('Error triggering DAG:', error);
      }
      

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
