import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { eventsApi } from "../services/events";

function normalizeApiError(err, fallback) {
  return err?.response?.data?.detail || err?.message || fallback;
}

export const useEventsStore = defineStore("events", () => {
  const events = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const feedingEvents = computed(() => events.value.filter(e => e.event_type === "feeding"));
  const sleepEvents = computed(() => events.value.filter(e => e.event_type === "sleep"));
  const diaperEvents = computed(() => events.value.filter(e => e.event_type === "diaper"));

  async function fetchEvents(babyId, params = {}) {
    if (!babyId) {
      events.value = [];
      return [];
    }
    
    isLoading.value = true;
    error.value = null;

    try {
      const data = await eventsApi.listEvents(babyId, params);
      events.value = data;
      return data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar eventos");
      console.error("Error fetching events:", err);
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  async function createEvent(babyId, eventData) {
    error.value = null;
    try {
      const newEvent = await eventsApi.createEvent(babyId, eventData);
      // Re-fetch or add to list (re-fetch is safer for ordering)
      await fetchEvents(babyId);
      return newEvent;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al crear evento");
      throw err;
    }
  }

  async function updateEvent(babyId, eventId, eventData) {
    error.value = null;
    try {
      const updatedEvent = await eventsApi.updateEvent(babyId, eventId, eventData);
      await fetchEvents(babyId);
      return updatedEvent;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al actualizar evento");
      throw err;
    }
  }

  async function deleteEvent(babyId, eventId) {
    error.value = null;
    try {
      await eventsApi.deleteEvent(babyId, eventId);
      events.value = events.value.filter(e => e.id !== eventId);
    } catch (err) {
      error.value = normalizeApiError(err, "Error al eliminar evento");
      throw err;
    }
  }

  return {
    events,
    isLoading,
    error,
    feedingEvents,
    sleepEvents,
    diaperEvents,
    fetchEvents,
    createEvent,
    updateEvent,
    deleteEvent,
  };
});
