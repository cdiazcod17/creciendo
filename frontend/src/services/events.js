import { http } from "./http";

export const eventsApi = {
  async listEvents(babyId, params = {}) {
    const response = await http.get(`/babies/${babyId}/events/`, { params });
    return response.data;
  },

  async createEvent(babyId, eventData) {
    const response = await http.post(`/babies/${babyId}/events/`, eventData);
    return response.data;
  },

  async getEvent(babyId, eventId) {
    const response = await http.get(`/babies/${babyId}/events/${eventId}`);
    return response.data;
  },

  async updateEvent(babyId, eventId, eventData) {
    const response = await http.patch(`/babies/${babyId}/events/${eventId}`, eventData);
    return response.data;
  },

  async deleteEvent(babyId, eventId) {
    await http.delete(`/babies/${babyId}/events/${eventId}`);
  },
};
