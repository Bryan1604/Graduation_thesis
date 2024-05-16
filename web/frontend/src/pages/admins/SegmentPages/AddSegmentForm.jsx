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
import { getAddress, deleteAddress, createAddress } from "../../../services/admin/addressShop";
import { toast } from "react-toastify";
import { createSegment } from "../../../services/admin/segment";

const cx = classNames.bind(styles);

export const AddSegmentForm = () => {
  const navigateTo = useNavigate();

  const [showCancelModal, setShowCancelModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);

  const handleShowErrorModal = () => setShowErrorModal(true);
  const [errorText, setErrorText] = useState("");
  const handleCloseCancelModal = () => setShowCancelModal(false);

  const handleCancel = () => {
    setShowCancelModal(true);
  };

  const handleConfirmCancel = () => {
    // Thực hiện hành động hủy tạo category ở đây
    setShowCancelModal(false);
    navigateTo("/admin/segments");
  };

  const [conditions, setCondition] = useState(["gender", "birthday", "place", "total_product_view", "total_purchase", "total_purchase_value", "min_purchase_view", "favorite_products"]);
  const [selectedCondition, setSelectedCondition] = useState("");
  const [operators, setOperators] = useState(["EQUAL", "GREATER_THAN", "LESS_THAN", "GREATER_OR_EQUAL", "LESS_OR_EQUAL", "INCLUDES", "NOT_EQUAL", "NOT_INCLUDES" ]);
  const [selectedOperator, setSelectedOperator] = useState("");
  const [types, setTypes] = useState(["INTEGER", "LONG", "FLOAT", "TIMESTAMP", "STRING", "DATETIME", "BOOLEAN"]);
  const [selectedType, setSelectedType] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      // try {
      //   const response = await axios.get("https://raw.githubusercontent.com/kenzouno1/DiaGioiHanhChinhVN/master/data.json");
      //   setCities(response.data);
      // } catch (error) {
      //   console.error("Error fetching data:", error);
      // }
      setCondition(["gender", "birthday", "place", "total_product_view", "total_purchase", "total_purchase_value", "min_purchase_view", "favorite_products"]);
      setTypes(["INTEGER", "LONG", "FLOAT", "TIMESTAMP", "STRING", "DATETIME", "BOOLEAN"]);
      setOperators(["EQUAL", "GREATER_THAN", "LESS_THAN", "GREATER_OR_EQUAL", "LESS_OR_EQUAL", "INCLUDES", "NOT_EQUAL", "NOT_INCLUDES" ]);
    };

    fetchData();
  }, []);

  const handleConditionChange = (e) => {
    const conditionName = e.target.value;
    const selectedConditionIndex = conditions.findIndex((condition) => condition === conditionName);
    setSelectedCondition( conditions[selectedConditionIndex]);
    formik.setFieldValue("condition", selectedCondition);
  };
  const handleOperatorChange = (e) => {
    const operatorName = e.target.value;
    const selectedOperatorIndex = operators.find((operator) => operator === operatorName);
    setSelectedOperator(operators[selectedOperatorIndex])
    formik.setFieldValue("operator", operatorName);
    console.log(selectedOperator)
  };
  const handleTypeChange = (e) => {
    const typeName = e.target.value;
    const selectedTypeIndex = operators.find((type) => type === type);
    setSelectedType( operators[selectedTypeIndex])
    formik.setFieldValue("type", typeName);
    console.log(selectedType)
  };

  const formik = useFormik({
    initialValues: {
      segment_name: "", 
      condition: "",
      operator: "",
      type: "",
      value: "",
    },
    validationSchema: Yup.object({
      segment_name: Yup.string().required("Bạn chưa nhập tên Phân khúc"),
      condition: Yup.string().required("Vui lòng nhập điều kiện phân khúc)"),
      operator: Yup.string().required("Bạn chưa chọn toán tử"),
      type: Yup.string().required("Bạn chưa chọn kiểu giá trị"),
      value: Yup.string().required("Bạn chưa nhập giá trị phân khúc"),
    }),
    onSubmit: (values) => {
      const rule = {
        condition: values.condition,
        operator: values.operator,
        type: values.type,
        value: values.value,
      }
      const dataToSend = {
        segment_name: values.segment_name,
        rule: JSON.stringify([
          rule
        ]),
      };
      try {
        createSegment(dataToSend.segment_name, dataToSend.rule);
        toast.success("Đã thêm phân khúc thành công");
        navigateTo("/admin/segments");
      } catch (error) {
        toast.error("Thêm phân khúc thất bại");
        console.error("Create segments fails:", error);
      }
      console.log(dataToSend);
      navigateTo('/admin/segments');
    },
    //call api trong onsubmit
    /*async (values) => {
            try {
                const res = await fetch("");
                ...
                res.error && setErrorText(res.error); 
                handleShowErrorModal(); //Show model thông báo lỗi
            }catch(error){
            }}
            navigate('/admin/stores');
        */
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
            <label htmlFor="address" className={cx("form-label")}>
              Tên phân khúc<span>*</span>
            </label>
            <input id={cx("address")} name="segment_name" type="text" placeholder="Tên phân khúc" value={formik.values.segment_name} onChange={formik.handleChange} className={cx("form-control")} />
            {formik.errors.segment_name && formik.touched.segment_name && <span className={cx("form-message")}>{formik.errors.segment_name}</span>}
          </div>

          <div className={cx("slt")}>
            <div>
              <select value={formik.values.condition} onChange={handleConditionChange}>
                <option value="" disabled>
                  Chọn điều kiện
                </option>
                {conditions.map((condition) => (
                  <option key={condition} value={condition}>
                    {condition}
                  </option>
                ))}
              </select>
              {formik.errors.condition && formik.touched.condition && (
                <span className={cx("form-message")}>
                  <br></br>
                  {formik.errors.condition}
                </span>
              )}
            </div>
            <div>
              <select value={formik.values.operator} onChange={handleOperatorChange}>
                <option value="" disabled>
                  Chọn toán tử
                </option>
                {operators.map((operator) => (
                  <option key={operator} value={operator}>
                    {operator}
                  </option>
                ))}
              </select>
              {formik.errors.operator && formik.touched.operator && (
                <span className={cx("form-message")}>
                  <br></br>
                  {formik.errors.operator}
                </span>
              )}
            </div>
            <div>
              <select value={formik.values.type} onChange={handleTypeChange}>
                <option value="" disabled>
                  Chọn kiểu dữ liệu
                </option>
                {types.map((type) => (
                  <option key={type} value={type}>
                    {type}
                  </option>
                ))}
              </select>
              {formik.errors.type && formik.touched.type && (
                <span className={cx("form-message")}>
                  <br></br>
                  {formik.errors.type}
                </span>
              )}
            </div>
          </div>

          <div className={cx("form-input")}>
            <label htmlFor="address" className={cx("form-label")}>
              Giá trị cho phân khúc<span>*</span>
            </label>
            <input id={cx("address")} name="value" type="text" placeholder="Giá trị cho phân khúc" value={formik.values.value} onChange={formik.handleChange} className={cx("form-control")} />
            {formik.errors.value && formik.touched.value && <span className={cx("form-message")}>{formik.errors.value}</span>}
          </div>

          <div className={cx("btn")}>
            <button className={cx("cancel")} onClick={handleCancel}>
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
        <Modal.Body>Bạn có chắc chắn muốn hủy tạo danh mục sản phẩm không?</Modal.Body>
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
          <Modal.Title>Lỗi khi thêm danh mục</Modal.Title>
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
