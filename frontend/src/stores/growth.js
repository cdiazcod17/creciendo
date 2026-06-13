import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { growthApi } from "../services/growth";

function normalizeApiError(err, fallback) {
  return err?.response?.data?.detail || err?.message || fallback;
}

export const useGrowthStore = defineStore("growth", () => {
  const records = ref([]);
  // Mapa para cachear registros por bebé: { babyId: [registros] }
  const recordsByBaby = ref({});
  const isLoading = ref(false);
  const error = ref(null);

  const sortedRecords = computed(() => {
    return [...records.value].sort((a, b) => new Date(b.measured_at) - new Date(a.measured_at));
  });

  const getLatestRecordByBabyId = (babyId) => {
    const list = recordsByBaby.value[babyId] || [];
    if (!list.length) return null;
    return [...list].sort((a, b) => new Date(b.measured_at) - new Date(a.measured_at))[0];
  };

  async function fetchRecords(babyId) {
    if (!babyId) return;
    isLoading.value = true;
    error.value = null;
    try {
      const data = await growthApi.listRecords(babyId);
      records.value = data;
      recordsByBaby.value[babyId] = data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar registros de crecimiento");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function fetchRecordsForMultipleBabies(babies) {
    if (!babies || babies.length === 0) return;
    isLoading.value = true;
    try {
      await Promise.all(
        babies.map(async (baby) => {
          const data = await growthApi.listRecords(baby.id);
          recordsByBaby.value[baby.id] = data;
        })
      );
    } catch (err) {
      console.error("Error en carga agregada de crecimiento", err);
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
    recordsByBaby,
    isLoading,
    error,
    sortedRecords,
    getLatestRecordByBabyId,
    fetchRecords,
    fetchRecordsForMultipleBabies,
    createRecord,
    updateRecord,
    deleteRecord,
  };
});
