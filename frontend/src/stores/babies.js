import { ref } from "vue";
import { defineStore } from "pinia";
import { babiesApi } from "../services/babies";

function normalizeError(error, fallback) {
  return error?.response?.data?.detail || fallback;
}

export const useBabiesStore = defineStore("babies", () => {
  const babies = ref([]);
  const baby = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  async function fetchBabies() {
    isLoading.value = true;
    error.value = null;

    try {
      babies.value = await babiesApi.list();
    } catch (err) {
      error.value = normalizeError(err, "No se pudieron cargar los bebés.");
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchBaby(babyId) {
    if (!babyId) {
      baby.value = null;
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      baby.value = await babiesApi.get(babyId);
    } catch (err) {
      error.value = normalizeError(err, "No se pudo cargar el bebé.");
      baby.value = null;
    } finally {
      isLoading.value = false;
    }
  }

  async function createBaby(payload) {
    isLoading.value = true;
    error.value = null;

    try {
      const created = await babiesApi.create(payload);
      babies.value.unshift(created);
      return created;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo crear el bebé.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateBaby(babyId, payload) {
    isLoading.value = true;
    error.value = null;

    try {
      const updated = await babiesApi.update(babyId, payload);
      baby.value = updated;
      babies.value = babies.value.map((item) => (item.id === updated.id ? updated : item));
      return updated;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo actualizar el bebé.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteBaby(babyId) {
    isLoading.value = true;
    error.value = null;

    try {
      await babiesApi.remove(babyId);
      babies.value = babies.value.filter((item) => item.id !== babyId);
      if (baby.value?.id === babyId) {
        baby.value = null;
      }
    } catch (err) {
      error.value = normalizeError(err, "No se pudo borrar el bebé.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    babies,
    baby,
    isLoading,
    error,
    fetchBabies,
    fetchBaby,
    createBaby,
    updateBaby,
    deleteBaby,
  };
});
