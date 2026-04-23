import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { appointmentsApi } from "../services/appointments";
import { useBabiesStore } from "./babies";

function normalizeError(error, fallback) {
  return error?.response?.data?.detail || fallback;
}

export const useAppointmentsStore = defineStore("appointments", () => {
  const babiesStore = useBabiesStore();
  
  // Mapa para cachear citas por bebé: { babyId: [citas] }
  const appointmentsByBaby = ref({});
  const isLoading = ref(false);
  const error = ref(null);

  // ALIAS RETROCOMPATIBLE: Expone las citas del bebé seleccionado actualmente
  const appointments = computed(() => {
    const id = babiesStore.activeBabyId;
    return id ? (appointmentsByBaby.value[id] || []) : [];
  });

  /**
   * Obtiene la cita futura más cercana para un bebé.
   */
  const getNextAppointmentByBabyId = (babyId) => {
    const list = appointmentsByBaby.value[babyId] || [];
    const now = new Date();
    
    return list
      .filter(app => new Date(app.scheduled_at) > now && app.status !== 'cancelled')
      .sort((a, b) => new Date(a.scheduled_at) - new Date(b.scheduled_at))[0] || null;
  };

  async function fetchAppointments(babyId) {
    if (!babyId) return [];
    
    isLoading.value = true;
    error.value = null;

    try {
      const data = await appointmentsApi.list(babyId);
      appointmentsByBaby.value[babyId] = data;
      return data;
    } catch (err) {
      error.value = normalizeError(err, "No se pudieron cargar las citas.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Carga masiva para el Dashboard
   */
  async function fetchAppointmentsForMultipleBabies(babies) {
    if (!babies || babies.length === 0) return;
    
    isLoading.value = true;
    try {
      await Promise.all(
        babies.map(baby => fetchAppointments(baby.id))
      );
    } catch (err) {
      console.error("Error en carga agregada de citas", err);
    } finally {
      isLoading.value = false;
    }
  }

  async function createAppointment(babyId, payload) {
    isLoading.value = true;
    try {
      const created = await appointmentsApi.create(babyId, payload);
      await fetchAppointments(babyId);
      return created;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo crear la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateAppointment(babyId, appointmentId, payload) {
    isLoading.value = true;
    try {
      const updated = await appointmentsApi.update(babyId, appointmentId, payload);
      await fetchAppointments(babyId);
      return updated;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo actualizar la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteAppointment(babyId, appointmentId) {
    isLoading.value = true;
    try {
      await appointmentsApi.remove(babyId, appointmentId);
      if (appointmentsByBaby.value[babyId]) {
        appointmentsByBaby.value[babyId] = appointmentsByBaby.value[babyId].filter(i => i.id !== appointmentId);
      }
    } catch (err) {
      error.value = normalizeError(err, "No se pudo eliminar la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    appointments,
    appointmentsByBaby,
    isLoading,
    error,
    getNextAppointmentByBabyId,
    fetchAppointments,
    fetchAppointmentsForMultipleBabies,
    createAppointment,
    updateAppointment,
    deleteAppointment,
  };
});
