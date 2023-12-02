const connection = require("../database/connectDB")

const categoriesController = {
    getAll: async (req, res) => {
        try {
            const [rows, fields] = await connection.promise().query(
                `select * from categories
            `)
            res.json({
                data: rows,
            })
        } catch (error) {
            console.log(error)
            res.json({
                state: "error",
            })
        }
    },
    getById: async (req, res) => {
        try {
            const { category_id } = req.params;
            const [rows, fields] = await connection.promise().query(`select * from categories where categoryId = ?`, [category_id]);
            res.json({
                data: rows,
            });
            // console.log(rows.length);
        } catch (error) {
            console.log(error);
            res.json({
                state: "error",
            });
        }
    },
    create: async (req, res) => {
        try {
            const { name } = req.body;

            const checkNameSql = "select * from categories where name = ?"
            const [nameRows, nameFields] = await connection.promise().query(checkNameSql, [name]);

            if (nameRows.length > 0) {
                return res.json({
                    error: "name already exist",
                })
            }

            const query = "insert into categories ( name) values (?)";
            const [rows, fields] = await connection.promise().query(query, [name]);
            res.json({
                message: "successful",
                data: rows,
            });

        } catch (error) {
            console.log(error);
            res.json({
                state: "error"
            });
        }
    },
    update: async (req, res) => {
        try {
            const { category_id } = req.params;
            console.log("id: " + req.params);

            const { name } = req.body;
            const query = 'UPDATE categories SET name = ? WHERE categoryId = ?';

            const [rows, fields] = await connection.promise().query(query, [name, category_id]);
            res.json({
                data: rows,
                message: "update success",
            });
        } catch (error) {
            console.log(error);
            res.json({
                state: "error"
            });
        }
    },
    delete: async (req, res) => {
        try {
            const { category_id } = req.params;
            const [rows, fields] = await connection.promise().query("delete from categories where categoryId = ?", [category_id]);
            res.json({
                message: "successful",
                data: rows,
            });
        } catch (error) {
            console.log(error);
            res.json({
                state: "error"
            });
        }
    }
}

module.exports = categoriesController