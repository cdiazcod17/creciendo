import { ref, computed } from "vue";
import { defineStore } from "pinia";

import { babiesApi } from "../services/babies";
import { useAuthStore } from "./auth";

function normalizeApiError(err, fallback) {
  return err?.response?.data?.detail || err?.message || fallback;
}

export const useBabiesStore = defineStore("babies", () => {
  const babies = ref([]);
  const baby = ref(null);
  const activeBabyId = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  const activeBaby = computed(() => {
    return babies.value.find((item) => item.id === activeBabyId.value) || null;
  });

  const hasBabies = computed(() => babies.value.length > 0);

  async function fetchBabies(userActiveBabyId = null) {
    isLoading.value = true;
    error.value = null;

    const authStore = useAuthStore();

    try {
      const data = await babiesApi.listBabies();
      babies.value = data;

      // Handle active baby selection synchronization
      const currentId = activeBabyId.value;
      const validBackendId = userActiveBabyId && data.some((item) => item.id === userActiveBabyId);
      const validCurrentId = currentId && data.some((item) => item.id === currentId);

      if (validBackendId) {
        activeBabyId.value = userActiveBabyId;
      } else if (!validCurrentId && data.length > 0) {
        activeBabyId.value = data[0].id;
      } else if (!validCurrentId) {
        activeBabyId.value = null;
      }

      return data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar bebés");
      console.error("Error fetching babies:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchBaby(babyId) {
    if (!babyId) {
      baby.value = null;
      return null;
    }

    isLoading.value = true;
    error.value = null;

    try {
      const data = await babiesApi.getBaby(babyId);
      baby.value = data;
      return data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar bebé");
      console.error("Error fetching baby:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function createBaby(babyData) {
    error.value = null;

    try {
      const newBaby = await babiesApi.createBaby(babyData);
      babies.value = [newBaby, ...babies.value];

      if (babies.value.length === 1 && !activeBabyId.value) {
        await setActiveBaby(newBaby.id, true);
      }

      return newBaby;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al crear bebé");
      throw err;
    }
  }

  async function setActiveBaby(babyId, persist = false) {
    if (!babyId) {
      activeBabyId.value = null;
      return;
    }

    activeBabyId.value = babyId;

    if (persist) {
      try {
        await babiesApi.setActiveBaby(babyId);
      } catch (err) {
        console.error("Error persisting active baby:", err);
        // Optionally handle error, maybe keep local selection if it's fine
      }
    }
  }

  async function updateBaby(babyId, babyData) {
    error.value = null;

    try {
      const updatedBaby = await babiesApi.updateBaby(babyId, babyData);
      const index = babies.value.findIndex((item) => item.id === babyId);

      if (index !== -1) {
        babies.value[index] = updatedBaby;
      }

      if (baby.value?.id === babyId) {
        baby.value = updatedBaby;
      }

      return updatedBaby;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al actualizar bebé");
      throw err;
    }
  }

  async function deleteBaby(babyId) {
    error.value = null;

    try {
      await babiesApi.deleteBaby(babyId);

      babies.value = babies.value.filter((item) => item.id !== babyId);

      if (baby.value?.id === babyId) {
        baby.value = null;
      }

      if (activeBabyId.value === babyId) {
        activeBabyId.value = null;
      }
    } catch (err) {
      error.value = normalizeApiError(err, "Error al eliminar bebé");
      throw err;
    }
  }

  return {
    babies,
    baby,
    activeBabyId,
    activeBaby,
    isLoading,
    error,
    hasBabies,
    fetchBabies,
    fetchBaby,
    createBaby,
    setActiveBaby,
    updateBaby,
    deleteBaby,
  };
});