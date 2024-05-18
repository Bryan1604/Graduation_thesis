import request from "../../utils/httpRequest";

export const getSegment = async () => {
  try {
    const res = await request.get("/segment/", {
      params: {},
    });
    console.log(res.data.data);
    return res.data.data;
  } catch (error) {
    console.log("getSegment " + error);
  }
};
export const deleteSegment = async (id) => {
  try {
    const res = await request.delete(`/segment/${id}`, {
      params: {},
    });
    return res.data.data;
  } catch (error) {
    console.log("getSegment " + error);
  }
};
export const createSegment = async (segment_name, rule) => {
  try {
    const res = await request.post("/segment/", {
        segment_name,
        rule
    });
    console.log(res.data);
    return res.data;
  } catch (error) {
    console.log("getSegment " + error);
  }
};

export const getOneSegment = async (id) => {
  try {
    const res = await request.get(`/segment/${id}`, {
      params: {},
    });
    return res.data;
  }
  catch (error) {
    console.log("getOneSegment " + error);
  }
};
