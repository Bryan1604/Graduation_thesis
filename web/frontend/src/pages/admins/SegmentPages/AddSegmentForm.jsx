import classNames from "classnames/bind";
import styles from "./AddSegmentForm.module.scss";
import { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";
import axios from "axios";
import { useFormik } from "formik";
import { Modal, Button } from "react-bootstrap";
import * as Yup from "yup";
import { toast } from "react-toastify";
import { createSegment } from "../../../services/admin/segment";
import { faTrashAlt } from "@fortawesome/free-solid-svg-icons";

const cx = classNames.bind(styles);

export const AddSegmentForm = () => {
  const navigateTo = useNavigate();

  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  const [errorText, setErrorText] = useState("");
  
  const [conditions, setConditions] = useState([{ condition: "", operator: "", type: "", value: "" }]);
  const [conditionOptions, setConditionOptions] = useState([]);
  const [operatorOptions, setOperatorOptions] = useState([]);
  const [typeOptions, setTypeOptions] = useState([]);

  const handleShowErrorModal = () => setShowErrorModal(true);
  const handleCloseCancelModal = () => setShowCancelModal(false);

  const handleCancel = () => {
    setShowCancelModal(true);
  };

  const handleConfirmCancel = () => {
    setShowCancelModal(false);
    navigateTo("/admin/segments");
  };

  useEffect(() => {
    const fetchData = async () => {
      // Fetch or set the condition, operator, and type options here
      setConditionOptions(["gender", "birthday", "place", "total_product_view", "total_purchase", "total_purchase_value", "min_purchase_value", "favorite_products"]);
      setOperatorOptions(["EQUAL", "GREATER_THAN", "LESS_THAN", "GREATER_OR_EQUAL", "LESS_OR_EQUAL", "INCLUDES", "NOT_EQUAL", "NOT_INCLUDES"]);
      setTypeOptions(["INTEGER", "LONG", "FLOAT", "TIMESTAMP", "STRING", "DATE", "BOOLEAN"]);
    };

    fetchData();
  }, []);

  const handleConditionChange = (e, index) => {
    const newConditions = [...conditions];
    newConditions[index].condition = e.target.value;
    setConditions(newConditions);
  };

  const handleOperatorChange = (e, index) => {
    const newConditions = [...conditions];
    newConditions[index].operator = e.target.value;
    setConditions(newConditions);
  };

  const handleTypeChange = (e, index) => {
    const newConditions = [...conditions];
    newConditions[index].type = e.target.value;
    setConditions(newConditions);
  };

  const handleValueChange = (e, index) => {
    const newConditions = [...conditions];
    newConditions[index].value = e.target.value;
    setConditions(newConditions);
  };

  const handleAddCondition = () => {
    setConditions([...conditions, { condition: "", operator: "", type: "", value: "" }]);
  };

  const handleDeleteCondition = (index) => {
    const newConditions = conditions.filter((_, i) => i !== index);
    setConditions(newConditions);
  };

  const formik = useFormik({
    initialValues: {
      segment_name: "",
    },
    validationSchema: Yup.object({
      segment_name: Yup.string().required("Bạn chưa nhập tên Phân khúc"),
      // Additional validation can be added for each condition field if needed
    }),
    onSubmit: (values) => {
      const dataToSend = {
        segment_name: values.segment_name,
        rule: JSON.stringify(conditions),
      };
      try {
        createSegment(dataToSend.segment_name, dataToSend.rule);
        toast.success("Đã thêm phân khúc thành công");
        navigateTo("/admin/segments");
      } catch (error) {
        toast.error("Thêm phân khúc thất bại");
        console.error("Create segments fails:", error);
      }
    },
  });

  return (
    <div className={cx("container")}>
      <div className={cx("nav")}>
        <Link to="/admin/segments" className={cx("back")}>
          <FontAwesomeIcon icon={faArrowLeft} style={{ paddingRight: "10px" }} />
          Quay lại danh sách các phân khúc
        </Link>
      </div>
      <form action="" method="POST" className={cx("form")} onSubmit={formik.handleSubmit} id={cx("form-1")}>
        <div className={cx("form-group")}>
          <div className={cx("form-input")}>
            <label htmlFor="segment_name" className={cx("form-label")}>
              Tên phân khúc<span>*</span>
            </label>
            <input
              id={cx("segment_name")}
              name="segment_name"
              type="text"
              placeholder="Tên phân khúc"
              value={formik.values.segment_name}
              onChange={formik.handleChange}
              className={cx("form-control")}
            />
            {formik.errors.segment_name && formik.touched.segment_name && (
              <span className={cx("form-message")}>{formik.errors.segment_name}</span>
            )}
          </div>

          {conditions.map((condition, index) => (
            <div key={index} className={cx("slt")}>
              <div>
                <select value={condition.condition} onChange={(e) => handleConditionChange(e, index)}>
                  <option value="" disabled>
                    Chọn điều kiện
                  </option>
                  {conditionOptions.map((conditionOption) => (
                    <option key={conditionOption} value={conditionOption}>
                      {conditionOption}
                    </option>
                  ))}
                </select>
                {formik.errors.condition && formik.touched.condition && (
                  <span className={cx("form-message")}>
                    <br />
                    {formik.errors.condition}
                  </span>
                )}
              </div>
              <div>
                <select value={condition.operator} onChange={(e) => handleOperatorChange(e, index)}>
                  <option value="" disabled>
                    Chọn toán tử
                  </option>
                  {operatorOptions.map((operatorOption) => (
                    <option key={operatorOption} value={operatorOption}>
                      {operatorOption}
                    </option>
                  ))}
                </select>
                {formik.errors.operator && formik.touched.operator && (
                  <span className={cx("form-message")}>
                    <br />
                    {formik.errors.operator}
                  </span>
                )}
              </div>
              <div>
                <select value={condition.type} onChange={(e) => handleTypeChange(e, index)}>
                  <option value="" disabled>
                    Chọn kiểu dữ liệu
                  </option>
                  {typeOptions.map((typeOption) => (
                    <option key={typeOption} value={typeOption}>
                      {typeOption}
                    </option>
                  ))}
                </select>
                {formik.errors.type && formik.touched.type && (
                  <span className={cx("form-message")}>
                    <br />
                    {formik.errors.type}
                  </span>
                )}
              </div>
              <div>
                <input
                  name={`value-${index}`}
                  type="text"
                  placeholder="Giá trị cho phân khúc"
                  value={condition.value}
                  onChange={(e) => handleValueChange(e, index)}
                  className={cx("form-control")}
                />
                {formik.errors.value && formik.touched.value && (
                  <span className={cx("form-message")}>{formik.errors.value}</span>
                )}
              </div>
              <div>
                <FontAwesomeIcon icon={faTrashAlt} style={{ cursor: "pointer", color: "red" }} onClick={() => handleDeleteCondition(index)} />
              </div>
            </div>
          ))}

          <button type="button" onClick={handleAddCondition} className={cx("form-submit")}>
            Thêm điều kiện
          </button>

          <div className={cx("btn")}>
            <button type="button" className={cx("cancel")} onClick={handleCancel}>
              Hủy
            </button>
            <button className={cx("form-submit")} type="submit" value="Submit Form">
              Tạo
            </button>
          </div>
        </div>
      </form>

      <Modal show={showCancelModal} onHide={handleCloseCancelModal}>
        <Modal.Header closeButton>
          <Modal.Title>Xác nhận hủy</Modal.Title>
        </Modal.Header>
        <Modal.Body>Bạn có chắc chắn muốn hủy tạo phân khúc không?</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" className={cx("btn-close-modal")} style={{ backgroundColor: "#36a2eb" }} onClick={handleCloseCancelModal}>
            Đóng
          </Button>
          <Button variant="danger" onClick={handleConfirmCancel}>
            Hủy
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={showErrorModal} onHide={() => setShowErrorModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Lỗi khi thêm phân khúc</Modal.Title>
        </Modal.Header>
        <Modal.Body>Đã xảy ra lỗi:{errorText}. Vui lòng nhập lại</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowErrorModal(false)}>
            Đóng
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AddSegmentForm;
