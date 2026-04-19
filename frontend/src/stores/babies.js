import { ref, computed } from "vue";
import { defineStore } from "pinia";

import { babiesApi } from "../services/babies";

export const useBabiesStore = defineStore("babies", () => {
  const babies = ref([]);
  const activeBabyId = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  const activeBaby = computed(() => {
    return babies.value.find(baby => baby.id === activeBabyId.value) || null;
  });

  const hasBabies = computed(() => babies.value.length > 0);

  async function fetchBabies() {
    isLoading.value = true;
    error.value = null;
    try {
      const data = await babiesApi.listBabies();
      babies.value = data;
      // Set first baby as active if none is set
      if (data.length > 0 && !activeBabyId.value) {
        activeBabyId.value = data[0].id;
      }
    } catch (err) {
      error.value = err.message || "Error al cargar bebés";
      console.error("Error fetching babies:", err);
    } finally {
      isLoading.value = false;
    }
  }

  async function createBaby(babyData) {
    try {
      const newBaby = await babiesApi.createBaby(babyData);
      babies.value.push(newBaby);
      // Set as active if it's the first baby
      if (babies.value.length === 1) {
        activeBabyId.value = newBaby.id;
      }
      return newBaby;
    } catch (err) {
      error.value = err.message || "Error al crear bebé";
      throw err;
    }
  }

  function setActiveBaby(babyId) {
    activeBabyId.value = babyId;
  }

  async function updateBaby(babyId, babyData) {
    try {
      const updatedBaby = await babiesApi.updateBaby(babyId, babyData);
      const index = babies.value.findIndex(b => b.id === babyId);
      if (index !== -1) {
        babies.value[index] = updatedBaby;
      }
      return updatedBaby;
    } catch (err) {
      error.value = err.message || "Error al actualizar bebé";
      throw err;
    }
  }

  async function deleteBaby(babyId) {
    try {
      await babiesApi.deleteBaby(babyId);
      babies.value = babies.value.filter(b => b.id !== babyId);
      // If deleted baby was active, set another one as active
      if (activeBabyId.value === babyId && babies.value.length > 0) {
        activeBabyId.value = babies.value[0].id;
      } else if (babies.value.length === 0) {
        activeBabyId.value = null;
      }
    } catch (err) {
      error.value = err.message || "Error al eliminar bebé";
      throw err;
    }
  }

  return {
    babies,
    activeBabyId,
    activeBaby,
    isLoading,
    error,
    hasBabies,
    fetchBabies,
    createBaby,
    setActiveBaby,
    updateBaby,
    deleteBaby,
  };
});