import { http } from "./http";

export const authApi = {
  async register(payload) {
    const response = await http.post("/auth/register", payload);
    return response.data;
  },

  async login(payload) {
    const response = await http.post("/auth/login", payload);
    return response.data;
  },

  async me() {
    const response = await http.get("/auth/me");
    return response.data;
  },

  async logout(refreshToken) {
    await http.post("/auth/logout", { refresh_token: refreshToken });
  },
};
