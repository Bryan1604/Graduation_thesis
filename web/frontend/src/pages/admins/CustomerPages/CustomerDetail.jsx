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
    const [favoriteCategories, setFavoriteCategories] = useState([]);

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
                setFavoriteCategories(data.favoriteCategories);
            } catch (error) {
                console.error("Error fetching customer list:", error);
            }
        }
        getCustomer();
    }, []);

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
                            <div class={cx("info_item__title")}>Các loại sản phẩm yêu thích gần đây trong 3 ngày gần đây</div>
                            <div>
                                {favoriteCategories.map((category, index) => (
                                    <div key={index}>
                                        <a href={`/categories/${category}`} target="_blank" rel="noopener noreferrer">
                                            - {category}
                                        </a>
                                    </div>
                                ))}
                            </div>
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
        </div>
    );
};

export default CustomerDetail;
