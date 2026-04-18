import { http } from "./http";

export const authApi = {
  async register(payload) {
    const response = await http.post("/auth/register", payload);
    return response.data;
  },

  async login(payload) {
    const data = new URLSearchParams();
    data.append("username", payload.email);
    data.append("password", payload.password);

    const response = await http.post("/auth/login", data, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" }
    });
    return response.data;
  },

  async me() {
    const response = await http.get("/auth/me");
    return response.data;
  },

  async logout() {
    await http.post("/auth/logout");
  },
};