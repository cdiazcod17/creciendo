import { ref } from "vue";
import { defineStore } from "pinia";
import { appointmentsApi } from "../services/appointments";

function normalizeError(error, fallback) {
  return error?.response?.data?.detail || fallback;
}

export const useAppointmentsStore = defineStore("appointments", () => {
  const appointments = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  async function fetchAppointments(babyId) {
    if (!babyId) {
      appointments.value = [];
      return;
    }

    isLoading.value = true;
    error.value = null;

    try {
      appointments.value = await appointmentsApi.list(babyId);
    } catch (err) {
      error.value = normalizeError(err, "No se pudieron cargar las citas.");
    } finally {
      isLoading.value = false;
    }
  }

  async function createAppointment(babyId, payload) {
    if (!babyId) throw new Error("Falta el identificador del bebé.");

    isLoading.value = true;
    error.value = null;

    try {
      const created = await appointmentsApi.create(babyId, payload);
      appointments.value.unshift(created);
      return created;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo crear la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function updateAppointment(babyId, appointmentId, payload) {
    if (!babyId || !appointmentId) throw new Error("Faltan datos para actualizar la cita.");

    isLoading.value = true;
    error.value = null;

    try {
      const updated = await appointmentsApi.update(babyId, appointmentId, payload);
      appointments.value = appointments.value.map((item) => (item.id === updated.id ? updated : item));
      return updated;
    } catch (err) {
      error.value = normalizeError(err, "No se pudo actualizar la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function deleteAppointment(babyId, appointmentId) {
    if (!babyId || !appointmentId) throw new Error("Faltan datos para eliminar la cita.");

    isLoading.value = true;
    error.value = null;

    try {
      await appointmentsApi.remove(babyId, appointmentId);
      appointments.value = appointments.value.filter((item) => item.id !== appointmentId);
    } catch (err) {
      error.value = normalizeError(err, "No se pudo eliminar la cita.");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    appointments,
    isLoading,
    error,
    fetchAppointments,
    createAppointment,
    updateAppointment,
    deleteAppointment,
  };
});
