import { http } from "./http";

export const growthApi = {
  async listRecords(babyId) {
    const response = await http.get(`/babies/${babyId}/growth-records/`);
    return response.data;
  },

  async createRecord(babyId, data) {
    const response = await http.post(`/babies/${babyId}/growth-records/`, data);
    return response.data;
  },

  async updateRecord(babyId, recordId, data) {
    const response = await http.patch(`/babies/${babyId}/growth-records/${recordId}`, data);
    return response.data;
  },

  async deleteRecord(babyId, recordId) {
    await http.delete(`/babies/${babyId}/growth-records/${recordId}`);
  },
};
