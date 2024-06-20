const fetch = require('node-fetch');
const express = require("express");
const app = express();
const cors = require("cors");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");

app.use(bodyParser.json()); // for parsing application/json
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cors({ credentials: true, origin: true }));
app.use(cookieParser());
//Tạo bảng
require("./modules/customerModule");
require("./modules/maGiamGia");
require("./modules/addressShop");
require("./modules/size");
require("./modules/categories");
require("./modules/product");
require("./modules/cardItem");
require("./modules/order");
require("./modules/orderItem");
require("./modules/productSize");
require("./modules/codeProvince");

//Import router
const customerRouter = require("./routers/customerRouter");
const maGiamGiaRouter = require("./routers/maGiamGiaRouter");
const addressShopRouter = require("./routers/addressShopRouter");
const productRouter = require("./routers/productRouter");
const categoryRouter = require("./routers/categoriesRouter");
const sizeRouter = require("./routers/sizeRouter");
const cartRouter = require("./routers/cartRouter");
const orderRouter = require("./routers/orderRouter");
const codeProvinceRouter = require("./routers/codeProvinceRouter");
const segmentRouter = require("./routers/segmentRouter");
//API
app.use("/customer", customerRouter);
app.use("/maGiamGia", maGiamGiaRouter);
app.use("/address-shop", addressShopRouter);
app.use("/product", productRouter);
app.use("/size", sizeRouter);
app.use("/category", categoryRouter);
app.use("/cart", cartRouter);
app.use("/order", orderRouter);
app.use("/codeProvince", codeProvinceRouter);
app.use("/segment", segmentRouter);

// call to trigger DAG when server start already

app.listen(3000, async () => { 
    // Thông tin cấu hình của Airflow
      const AIRFLOW_API_URL = 'http://localhost:8082/api/v1';
      const AIRFLOW_USERNAME = 'admin';
      const AIRFLOW_PASSWORD = 'admin';

      const DAG_ID = 'streaming_event';
      
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
    } catch (error) {
        console.error('Error triggering DAG:', error);
    }
});
