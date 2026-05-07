import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { growthApi } from "../services/growth";

function normalizeApiError(err, fallback) {
  return err?.response?.data?.detail || err?.message || fallback;
}

export const useGrowthStore = defineStore("growth", () => {
  const records = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const sortedRecords = computed(() => {
    return [...records.value].sort((a, b) => new Date(b.measured_at) - new Date(a.measured_at));
  });

  async function fetchRecords(babyId) {
    if (!babyId) return;
    isLoading.value = true;
    error.value = null;
    try {
      const data = await growthApi.listRecords(babyId);
      records.value = data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar registros de crecimiento");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function createRecord(babyId, data) {
    error.value = null;
    try {
      const newRecord = await growthApi.createRecord(babyId, data);
      await fetchRecords(babyId);
      return newRecord;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al crear registro de crecimiento");
      throw err;
    }
  }

  async function updateRecord(babyId, recordId, data) {
    error.value = null;
    try {
      const updated = await growthApi.updateRecord(babyId, recordId, data);
      await fetchRecords(babyId);
      return updated;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al actualizar registro");
      throw err;
    }
  }

  async function deleteRecord(babyId, recordId) {
    error.value = null;
    try {
      await growthApi.deleteRecord(babyId, recordId);
      records.value = records.value.filter((r) => r.id !== recordId);
    } catch (err) {
      error.value = normalizeApiError(err, "Error al eliminar registro");
      throw err;
    }
  }

  return {
    records,
    isLoading,
    error,
    sortedRecords,
    fetchRecords,
    createRecord,
    updateRecord,
    deleteRecord,
  };
});
