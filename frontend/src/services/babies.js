import { http } from "./http";

export const babiesApi = {
  async listBabies() {
    const response = await http.get("/babies/");
    return response.data;
  },

  async createBaby(babyData) {
    const response = await http.post("/babies/", babyData);
    return response.data;
  },

  async getBaby(babyId) {
    const response = await http.get(`/babies/${babyId}`);
    return response.data;
  },

  async updateBaby(babyId, babyData) {
    const response = await http.patch(`/babies/${babyId}`, babyData);
    return response.data;
  },

  async deleteBaby(babyId) {
    await http.delete(`/babies/${babyId}`);
  },
};