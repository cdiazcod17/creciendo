import { computed, ref } from "vue";
import { defineStore } from "pinia";

import { authApi } from "../services/auth";

function normalizeApiError(error, fallback) {
  return error?.response?.data?.detail || fallback;
}

export const useAuthStore = defineStore("auth", () => {
  const user = ref(null);
  const isLoading = ref(false);
  const accessToken = ref(localStorage.getItem("access_token"));

  const isAuthenticated = computed(() => Boolean(accessToken.value));
  const hasActiveBaby = computed(() => Boolean(user.value?.active_baby_id));

  function setTokens(access, refresh) {
    localStorage.setItem("access_token", access);
    localStorage.setItem("refresh_token", refresh);
    accessToken.value = access;
  }

  function syncAccessTokenFromStorage() {
    accessToken.value = localStorage.getItem("access_token");
  }

  function persistUser(currentUser) {
    user.value = currentUser;
    if (currentUser) {
      localStorage.setItem("user", JSON.stringify(currentUser));
      return;
    }
    localStorage.removeItem("user");
  }

  function clearSession() {
    user.value = null;
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    accessToken.value = null;
  }

  async function register(payload) {
    isLoading.value = true;
    try {
      await authApi.register(payload);
      await login({ email: payload.email, password: payload.password });
    } finally {
      isLoading.value = false;
    }
  }

  async function login(payload) {
    isLoading.value = true;
    try {
      const tokenData = await authApi.login(payload);
      setTokens(tokenData.access_token, tokenData.refresh_token);
      await fetchCurrentUser();
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchCurrentUser() {
    const currentUser = await authApi.me();
    persistUser(currentUser);
    return currentUser;
  }

  function hydrateFromStorage() {
    syncAccessTokenFromStorage();
    const rawUser = localStorage.getItem("user");
    if (!rawUser) {
      return;
    }
    try {
      persistUser(JSON.parse(rawUser));
    } catch {
      localStorage.removeItem("user");
    }
  }

  async function logout() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (refreshToken) {
      try {
        await authApi.logout(refreshToken);
      } catch {
      }
    }

    clearSession();
  }

  return {
    user,
    isLoading,
    isAuthenticated,
    hasActiveBaby,
    register,
    login,
    fetchCurrentUser,
    hydrateFromStorage,
    logout,
    clearSession,
    normalizeApiError,
  };
});
