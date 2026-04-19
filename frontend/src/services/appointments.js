import { http } from "./http";

const appointmentsUrl = (babyId) => `/babies/${babyId}/appointments`;

export const appointmentsApi = {
  async list(babyId) {
    const response = await http.get(appointmentsUrl(babyId));
    return response.data;
  },

  async getNext(babyId) {
    const response = await http.get(`${appointmentsUrl(babyId)}/next`);
    return response.data;
  },

  async create(babyId, payload) {
    const response = await http.post(appointmentsUrl(babyId), payload);
    return response.data;
  },

  async update(babyId, appointmentId, payload) {
    const response = await http.patch(`${appointmentsUrl(babyId)}/${appointmentId}`, payload);
    return response.data;
  },

  async remove(babyId, appointmentId) {
    await http.delete(`${appointmentsUrl(babyId)}/${appointmentId}`);
  },
};
