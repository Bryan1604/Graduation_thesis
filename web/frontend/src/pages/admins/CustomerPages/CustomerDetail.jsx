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
            <div className={cx("container")}>
                <div className={cx("nav")} style={{ cursor: 'pointer', color: 'blue' }}>
                    <div onClick={goBack} className={cx("back")} style={{ cursor: 'pointer' }}>
                        <FontAwesomeIcon icon={faArrowLeft} style={{ paddingRight: "10px" }} />
                        Quay lại 
                    </div>
                </div>
                <div className={cx("basic-infomation")}>
                    <div class={cx("title")}>
                        <h1>Thông tin cơ bản</h1>
                    </div>
                    <div class={cx("info")}>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>TÊN</div>
                            <div class={cx("info_item__content")}>{customer.fullname}</div>
                        </div>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>EMAIL</div>
                            <div class={cx("info_item__content")}>{customer.email}</div>
                        </div>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>SỐ ĐIỆN THOẠI</div>
                            <div class={cx("info_item__content")}>{customer.phone_number}</div>
                        </div>
                    </div>
                    <div class={cx("more_info")}>
                        <div class={cx("more_info_item")}>
                            <div class={cx("more_info_item__title")}>NGÀY SINH</div>
                            <div class={cx("more_info_item__content")}>{customer.birthday ? formatDateTime(customer.birthday) : ""}</div>
                        </div>
                        <div class={cx("more_info_item")}>
                            <div class={cx("more_info_item__title")}>GIỚI TÍNH</div>
                            <div class={cx("more_info_item__content")}>{customer.gender == 0 ? 'Nam' : 'Nữ'}</div>
                        </div>
                        <div class={cx("more_info_item")}>
                            <div class={cx("more_info_item__title")}>ĐỊA CHỈ</div>
                            <div class={cx("more_info_item__content")}>{customer.place}</div>
                        </div>
                    </div>
                    {/* <h3>Thông tin cơ bản của khách hàng có id : {id}</h3>
                    <h4 className="title">Tên </h4>
                    <h5> {customer.fullname} </h5>
                    <h4 className="title">Giới tính  </h4>  
                    <h5> {customer.gender == 0 ? 'Nam' : 'Nữ'} </h5>
                    <h4 className="title">Ngày sinh  </h4> 
                    <h5>{customer.birthday ? formatDateTime(customer.birthday) : ""}</h5>
                    <h4 className="title">Email  </h4> 
                    <h5> {customer.email}</h5>
                    <h4 className="title">Số điện thoại  </h4>
                    <h5>{customer.phone_number}</h5>
                    <h4 className="title">Địa chỉ  </h4>
                    <h5> {customer.place} </h5> */}
                </div>
                <div className={cx("addition-infomation")}>
                    <div class={cx("title")}>
                        <h1>Thông tin bổ sung</h1>
                    </div>
                    <div class={cx("info")}>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>Các sản phẩm yêu thích :</div>
                            <div>
                                {favoriteProducts.map((product, index) => (
                                    <div key={index}>
                                        <a href={`/product/${product}`} target="_blank" rel="noopener noreferrer">
                                            - {product}
                                        </a>
                                    </div>
                                ))}
                            </div>
                        </div>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>Các loại sản phẩm yêu thích gần đây</div>
                            <div class={cx("info_item__content")}>{customer.email}</div>
                        </div>
                        
                    </div>
                    <div class={cx("info")}>
                        <div class={cx("info_item")}>
                            <div class={cx("info_item__title")}>Thông tin về các hoạt động </div>
                            <div class={cx("info_item__content")}>Số sản phẩm đã từng xem và quan tâm: {customer.product_count}</div>
                            <div class={cx("info_item__content")}>Tổng lượt xem các sản phẩm: {customer.total_view_count}</div>
                            <div class={cx("info_item__content")}>Số sản phẩm đã từng mua : {customer.total_purchase}</div>
                            <div class={cx("info_item__content")}>Tổng giá trị các đơn hàng đã mua : {customer.total_purchase_value}</div>
                            <div class={cx("info_item__content")}>Trung bình giá trị của 1 đơn hàng đã mua : {customer.avg_purchase_value}</div>
                            <div class={cx("info_item__content")}>Giá trị đơn hàng tối thiểu : {customer.min_purchase_value}</div>
                        </div>
                    </div>
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
