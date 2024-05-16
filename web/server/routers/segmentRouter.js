const express = require("express");
const router = express.Router();
const { authUser, authRoleAdmin, authRoleUser } = require("../middleware/auth");

const segmentController = require("../controllers/segmentController");

router.get("/", segmentController.getALL);
router.get("/:id", segmentController.getById);
router.post("/", authUser, authRoleAdmin, segmentController.create);
router.delete("/:id", authUser, authRoleAdmin, segmentController.delete);

module.exports = router;
