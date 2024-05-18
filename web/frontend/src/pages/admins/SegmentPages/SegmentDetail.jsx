import classNames from "classnames/bind";
import styles from "./SegmentList.module.scss";
import customStyles from "../ProductPages/CustomTable";
import { useEffect, useState } from "react";
import { Link , useParams} from "react-router-dom";
import DataTable from "react-data-table-component";
import { Modal, Button } from "react-bootstrap";
import { getSegment, deleteSegment, createSegment, getOneSegment } from "../../../services/admin/segment";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import { useNavigate } from "react-router-dom";
import {format, parseISO } from 'date-fns';

const cx = classNames.bind(styles);

const SegmentDetail = () => {
    const { id } = useParams();
    const navigateTo = useNavigate();
    const columns = [
        {
            name: "Id khách hàng",
            selector: (row) => row.customer_id,
            width: "15%",
        },
        {
            name: "Tên khách hàng",
            selector: (row) => row.fullname,
            width: "25%",
            sortable: true,
        },
        {
            name: "Email",
            selector: (row) => row.email,
            width: "20%",
            wrap: true,
        },
        {
            name: "Số điện thoại",
            selector: (row) => row.phone_number,
            width: "20%",
        },
        {
            name: "Chi tiết",
            cell: (row) =>
                <button onClick={() => viewCustomerDetail(row)} style={{ cursor: "pointer", backgroundColor: "transparent", border: "none", color: "blue", textDecoration: "underline" }}>
                    Xem chi tiết
                </button>,
            width: "20%",
        },
    ];

    const [segment, setSegment] = useState({ rule: [] });
    const [customers, setCustomers] = useState([]);

     // Hàm tải lại dữ liệu
    const reloadData = async () => {
        try {
            const data = await getOneSegment(id);
            if (data.segmentDetail.length > 0) {
                setSegment(data.segmentDetail[0]);
            }
            setCustomers(data.customers);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    };

    const viewCustomerDetail = (row) => {
        navigateTo(`/admin/customers/${row.customer_id}`);
    }

    const formatDateTime = (dateTimeString) => {
        try {
            const parsedDate = parseISO(dateTimeString);
            return format(parsedDate, 'yyyy-MM-dd HH:mm:ss');
        } catch (error) {
            console.error("Invalid date time value:", dateTimeString);
            return dateTimeString; // hoặc trả về giá trị gốc nếu không thể phân tích cú pháp
        }
    };

    // Sử dụng useEffect để tải dữ liệu ban đầu
    useEffect(() => {
        reloadData();
    }, [id]);

    return (
        <div className={cx("wrap")}>
            <div className={cx("nav")}>
                <Link to="/admin/segments" className={cx("back")}>
                <FontAwesomeIcon icon={faArrowLeft} style={{ paddingRight: "10px" }} />
                Quay lại danh sách các phân khúc
                </Link>
            </div>
            <div className={cx("cd-btn")}>
                <button className={cx("create-btn")} onClick={reloadData}>
                    Tải lại dữ liệu
                </button>
            </div>

            <div>
                <h3>Thông tin phân khúc</h3>
                <h5>Tên phân khúc : {segment.segment_name}</h5>
                {/* Hiển thị các rule */}
                    <div>
                        {segment.rule.map((r, index) => (
                            <div key={index}>
                                <h5>Điều kiện : {r.condition} {r.operator} {r.value}</h5>
                            </div>
                        ))}
                    </div>
                <h5>Thời gian khởi tạo : { segment.create_time ? formatDateTime(segment.create_time) : ""}</h5>
                <h5>Thời gian cập nhật : {segment.update_time ? formatDateTime(segment.update_time) : ""}</h5>
            </div>

            <DataTable
                columns={columns}
                data={customers}
                fixedHeader
                pagination
                customStyles={customStyles}
            ></DataTable>
            
        </div>
    );
};

export default SegmentDetail;
