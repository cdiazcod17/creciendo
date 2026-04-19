import { http } from "./http";

export const babiesApi = {
  async list() {
    const response = await http.get("/babies");
    return response.data;
  },

  async get(babyId) {
    const response = await http.get(`/babies/${babyId}`);
    return response.data;
  },

  async create(payload) {
    const response = await http.post("/babies", payload);
    return response.data;
  },

  async update(babyId, payload) {
    const response = await http.patch(`/babies/${babyId}`, payload);
    return response.data;
  },

  async remove(babyId) {
    await http.delete(`/babies/${babyId}`);
  },
};
