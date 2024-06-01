const connection = require("../database/connectDB");
const connection_cdp = require("../database/connectDB_CDP");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcrypt")

const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

const customerController = {
  getALL: async (req, res) => {
    try {
      const [rows, fields] = await connection.promise().query("select * from customers where role = 'user'");
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
      const [customerRows, fields] = await connection_cdp.promise().query(
        "select customers.*, (select count(product_id) from customer_product where customer_id = ?) as product_count,(select sum(view_count) from customer_product where customer_id = ?) as total_view_count from customers where customers.customer_id = ?", 
        [id, id, id]
      );
      if (customerRows.length === 0) {
      return res.status(404).json({ state: "error", message: "Customer not found" });
    }

    const customer = customerRows[0];

    // Lấy danh sách sản phẩm yêu thích
    const favoriteProductIds = customer.favorite_products ? customer.favorite_products.split(',') : [];
    let favoriteProducts = [];
    if (favoriteProductIds.length > 0) {
      const [productRows] = await connection_cdp.promise().query(
        "SELECT product_name FROM products WHERE product_id IN (?)",
        [favoriteProductIds]
      );
      favoriteProducts = productRows.map(row => row.product_name);
    }
      
    // Lay the loai yeu thich trong thoi gian gan day ( 3 ngay)
    let favoriteCategories = [];
    const [catrgoryRows] = await connection_cdp.promise().query(
      "SELECT cate.* FROM categories as cate, customer_category as cc WHERE cate.category_id = cc.category_id AND cc.customer_id = ?", [customer.customer_id]
    )
      
    favoriteCategories = catrgoryRows.map(row => row.category_name);

    res.json({
      data: customer,
      favoriteProducts: favoriteProducts,
      favoriteCategories: favoriteCategories,
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
      const { name, email, phone, password, role } = req.body;

      // check format email
      if (!emailRegex.test(email)) {
        return res.json({
          error: "Invalid email format",
        });
      }

      const checkEmailSql = "SELECT * FROM customers WHERE email = ?";
      const [emailRows, emailFields] = await connection.promise().query(checkEmailSql, [email]);

      if (emailRows.length > 0) {
        return res.json({
          error: "Email already exists",
        });
      } else {
        const hashedPassword = await bcrypt.hash(password, 10);
        const insertSql = "INSERT INTO customers (name, email, phone, password, role) VALUES (?, ?, ?, ?, ?)";
        const [rows, fields] = await connection.promise().query(insertSql, [name, email, phone, password, role]);
        res.json({
          data: rows,
        });
      }
    } catch (error) {
      console.log(error);
      res.json({
        state: "error",
      });
    }
  },
  update: async (req, res) => {
    try {
      const { name, email, phone, password } = req.body;
      const { id } = req.params;
      const sql = "update customers set name = ?,email = ?,phone = ?,password = ? where customerId = ?";
      const [rows, fields] = await connection.promise().query(sql, [name, email, phone, password, id]);
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
      const [rows, fields] = await connection.promise().query("delete from customers where customerId = ?", [id]);
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
  loginUser: async (req, res) => {
    try {
      const { email, password } = req.body;

      // Truy vấn kiểm tra email và mật khẩu
      // Truy vấn kiểm tra email
      const [rows] = await connection.promise().query("SELECT * FROM customers WHERE email = ?", [email]);

      if (rows.length === 1) {
        const storedPasswordHash = rows[0].password;

        // So sánh mật khẩu
        // const passwordMatch = await bcrypt.compare(password, storedPasswordHash);


        if (password == storedPasswordHash) {
          const role = rows[0].role;
          const name = rows[0].name;
          const phone = rows[0].phone;
          const id = rows[0].customerId;

          // Kiểm tra giá trị "role"
          if (role && role.toLowerCase() === "user") {
            const customer = {
              email: email,
              role: role,
              name: name,
              phone: phone,
              id: id
            };
            const token = jwt.sign(customer, "your-secret-key");
            res.header("Authorization", token);
            res.cookie("token", token, { secure: false, httpOnly: false });
            console.log("line 130", token);
            res.status(200).send({ message: "Login successful", token: token, user: customer });
          } else {
            if (role && role.toLowerCase() === "admin") {
              const customer = {
                email: email,
                role: role,
                name: name,
                phone: phone,
              };
              const token = jwt.sign(customer, "your-secret-key");
              res.header("Authorization", token);
              res.cookie("token", token, { secure: false, httpOnly: false });
              console.log("line 130", token);
              res.status(200).send({ message: "Login successful", token: token, user: customer });
            } else {
              res.status(200).json({ message: "fails", error: "Invalid role" });
            }
          }
        }
      } else {
        res.status(200).json({ message: "Email hoặc mật khẩu sai", error: "Login failed" });
      }
    } catch (error) {
      console.error(error);
      res.status(500).json({ error: "Internal server error" });
    }
  },

  verifyToken: (req, res) => {
    try {
      const { token } = req.body;
      console.log("line149", token);
      let kq = jwt.verify(token, "your-secret-key");
      console.log("JWT Token:", kq);
      if (kq != undefined) {
        res.json({ message: "Verify successful", data: kq });
      }
    } catch (error) {
      console.log("Chua dang nhap !");
      res.status(401).json({ message: "fails", error: "Login failed" });
    }
  },
  verifyTokenAdmin: (req, res) => {
    try {
      const { token } = req.body;
      console.log("line149", token);
      let kq = jwt.verify(token, "your-secret-key");
      console.log("JWT Token:", kq);
      if (kq != undefined) {
        res.json({ message: "Verify successful", data: kq });
      }
    } catch (error) {
      console.log("Chua dang nhap !");
      res.status(401).json({ message: "fails", error: "Login failed" });
    }
  },
};

module.exports = customerController;
