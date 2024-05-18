import classNames from "classnames/bind";
import styles from "./SegmentList.module.scss";
import customStyles from "../ProductPages/CustomTable";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import DataTable from "react-data-table-component";
import { Modal, Button } from "react-bootstrap";
import { getSegment, deleteSegment, createSegment } from "../../../services/admin/segment";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { format, parseISO } from 'date-fns';

const cx = classNames.bind(styles);

const SegmentList = () => {
  const navigateTo = useNavigate();
  const columns = [
    {
      name: "STT",
      selector: (row) => row.segment_id,
      width: "10%",
    },
    {
      name: "Tên phân khúc",
      selector: (row) => row.segment_name,
      width: "30%",
      sortable: true,
    },
    {
      name: "Thời gian tạo",
      selector: (row) => formatDateTime(row.create_time),
      width: "20%",
      wrap: true,
    },
    {
      name: "Thời gian cập nhật",
      selector: (row) => formatDateTime(row.update_time),
      width: "20%",
    },
    {
      name: "Tổng số khách hàng",
      selector: (row) => row.customer_count,
      width: "20%",
    },
  ];

  useEffect(() => {
    async function getAllSegment() {
      getSegment()
        .then((data) => {
          setSegments(data);
        })
        .catch((error) => console.error("Error fetching segments list:", error));
    }
    getAllSegment();
    setSelectedRows([]);
  }, []);

  const [segments, setSegments] = useState([]);
  const [selectedRows, setSelectedRows] = useState([]);
  const [clearSelect, setClearSelect] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);

  const handleCloseDeleteModal = () => setShowDeleteModal(false);
  const confirmDelete = () => {
    setShowDeleteModal(true);
  };

  const handleDelete = async () => {
    // Lấy danh sách ID của các cửa hàng đã chọn
    const segmentIdsToDelete = selectedRows.map((row) => row.segment_id);

    try {
      await Promise.all(segmentIdsToDelete.map((id) => deleteSegment(id)));
      // Nếu xóa thành công, cập nhật state với danh sách mới(loại bỏ các danh mục đã chọn)
      const updatedSegments = segments.filter((c) => !segmentIdsToDelete.includes(c.segment_id));
      setSegments(updatedSegments);

      // Đặt lại danh sách được chọn
      setClearSelect(!clearSelect);
      setSelectedRows([]);
      toast.success("Đã xóa phân khúc khách hàng!!");
    } catch (error) {
      console.error("Lỗi khi xóa phân khúc khách hang:", error.message);
      toast.error("Lỗi khi xóa phân khúc khách hàng!!");
    }
    setShowDeleteModal(false);
  };

  const handleRowClicked = (row) => {
    navigateTo(`/admin/segments/${row.segment_id}`);
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

  return (
    <div className={cx("wrap")}>
      <div className={cx("cd-btn")}>
        <button className={cx("delete-btn")} onClick={confirmDelete}>
          Xóa Phân khúc
        </button>
        <Link to="/admin/segments/add" className={cx("create-btn")}>
          Thêm phân khúc
        </Link>
      </div>

      <div>
        <h3>Danh sách Phân khúc</h3>
      </div>

      <DataTable
        columns={columns}
        data={segments}
        selectableRows
        fixedHeader
        pagination
        onSelectedRowsChange={({ selectedRows }) => {
          setSelectedRows(selectedRows);
          console.log(selectedRows);
        }}
        onRowClicked={handleRowClicked}  
        customStyles={customStyles}
        clearSelectedRows={clearSelect}
      ></DataTable>
      <Modal show={showDeleteModal} onHide={handleCloseDeleteModal}>
        <Modal.Header closeButton>
          <Modal.Title>Xác nhận hủy</Modal.Title>
        </Modal.Header>
        <Modal.Body>Bạn chắc chắn muốn xóa phân khúc khách hàng?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" className={cx("btn-close-modal")} style={{ backgroundColor: "#36a2eb" }} onClick={handleCloseDeleteModal}>
            Hủy
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            Xóa
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default SegmentList;
