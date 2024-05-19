import classNames from "classnames/bind";
import styles from "./CustomerDetail.module.scss";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { getOneCustomer} from "../../../services/admin/customer";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { format, parseISO } from 'date-fns';

const cx = classNames.bind(styles);

const CustomerDetail = () => {
    const navigate = useNavigate();
    const { id } = useParams();
    const [customer, setCustomer] = useState({});
    const [favoriteProducts, setFavoriteProducts] = useState([]);

    const goBack = () => {
        navigate(-1);
    }

    const formatDateTime = (dateTimeString) => {
        try {
            const parsedDate = parseISO(dateTimeString);
            return format(parsedDate, 'yyyy-MM-dd');
        } catch (error) {
            console.error("Invalid date time value:", dateTimeString);
            return dateTimeString; // hoặc trả về giá trị gốc nếu không thể phân tích cú pháp
        }
    };

    useEffect(() => {
        async function getCustomer() {
            try {
                const data = await getOneCustomer(id);
                setCustomer(data.data);
                setFavoriteProducts(data.favoriteProducts);
            } catch (error) {
                console.error("Error fetching customer list:", error);
            }
        }
        getCustomer();
    }, []);
    
    const favoriteProductsString = favoriteProducts.join(', ');

    return (
        <div>
            <div className="container">
                <div className={cx("nav")} style={{ cursor: 'pointer', color: 'blue' }}>
                    <div onClick={goBack} className={cx("back")} style={{ cursor: 'pointer' }}>
                        <FontAwesomeIcon icon={faArrowLeft} style={{ paddingRight: "10px" }} />
                        Quay lại 
                    </div>
                </div>
                <div className="left-pane">
                    <h3>Thông tin cơ bản của khách hàng có id : {id}</h3>
                    <h4>Tên : {customer.fullname} </h4>
                    <h4>Giới tính: {customer.gender == 0 ? 'Nam' : 'Nữ'} </h4>
                    <h4>Ngày sinh : {customer.birthday ? formatDateTime(customer.birthday) : ""}</h4>
                    <h4>Email : {customer.email}</h4>
                    <h4>Số điện thoại : {customer.phone_number}</h4>
                    <h4>Địa chỉ : {customer.place} </h4>
                </div>
                <div className="right-pane">
                    <h3>Thông tin bổ sung :</h3>
                    <h4>Các sản phẩm yêu thích : </h4>
                    <div>
                        {favoriteProducts.map((product, index) => (
                            <div key={index}>
                                <a href={`/product/${product}`} target="_blank" rel="noopener noreferrer">
                                    - {product}
                                </a>
                            </div>
                        ))}
                    </div>
                    <h4>Thể loại yêu thích : </h4>
                    <h4>Số sản phẩm đã từng xem : {customer.product_count}</h4>
                    <h4>Tổng lượt xem các sản phẩm: {customer.total_view_count}</h4>
                    <h4>Số sản phẩm đã từng mua : {customer.total_purchase}</h4>
                    <h4>Tổng giá trị các đơn hàng đã mua : {customer.total_purchase_value}</h4>
                    <h4>Trung bình giá trị của 1 đơn hàng đã mua : {customer.avg_purchase_value}</h4>
                    <h4>Giá trị đơn hàng tối thiểu : {customer.min_purchase_value}</h4>
                </div>
            </div>
            {/* <div className={cx("userList")}>
                <div className={cx("productDescription", "row")}>
                    <input className="productId" type="text" value={id} disabled style={{ display: "none" }} />
                    <div className={cx("divLeft", "col-12", "col-lg-6")}>
                        <img src="https://www.google.com/imgres?imgurl=https%3A%2F%2Fcellphones.com.vn%2Fsforum%2Fwp-content%2Fuploads%2F2023%2F10%2Fanh-avatar-facebook-7-1.jpg&tbnid=LAWh-_VNeRAAoM&vet=12ahUKEwiK0dq-7paGAxXrkK8BHbtyCBsQMygFegQIARB7..i&imgrefurl=https%3A%2F%2Fcellphones.com.vn%2Fsforum%2Fanh-avatar-facebook&docid=aTxttayw6IpBsM&w=850&h=850&q=avatar%20facebook&ved=2ahUKEwiK0dq-7paGAxXrkK8BHbtyCBsQMygFegQIARB7" alt="Item 1" />
                    </div>
                    <div className={cx("divRight", "col-xs-12", "col-lg-6")}>
                        <h3>Tên: </h3>
                        <span className={cx("product_id_1")}>Mã sản phẩm: <span className={cx("product_id")}>{id}</span></span><br></br>
                        <br></br>
                        <span className={cx("price")}>đ</span>

                        <div className={cx("select")}>
                            <label for="cars">Choose a size:</label>

                            <p>Số lượng:</p>
                        </div>
                        

                        <div className={cx("product_describe")}>
                            <div className={cx("product_describe_head")}>
                                <h5>Mô tả sản phẩm</h5>
                            </div>
                            <div className={cx("product_describe_body")}>
                                <p style={{
                                    fontWeight: 100,
                                    fontSize: '14px'
                                }}
                                >
                                    Hêo 
                                </p>
                            </div>

                        </div>

                    </div>
                </div>
            </div> */}
        </div>
    );
};

export default CustomerDetail;
