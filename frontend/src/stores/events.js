import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { eventsApi } from "../services/events";
import { useBabiesStore } from "./babies";

function normalizeApiError(err, fallback) {
  return err?.response?.data?.detail || err?.message || fallback;
}

export const useEventsStore = defineStore("events", () => {
  const babiesStore = useBabiesStore();
  
  // Mapa para cachear eventos por bebé: { babyId: [eventos] }
  const eventsByBaby = ref({});
  const isLoading = ref(false);
  const error = ref(null);

  // ALIAS RETROCOMPATIBLE: Expone los eventos del bebé seleccionado actualmente
  const events = computed(() => {
    const id = babiesStore.activeBabyId;
    return id ? (eventsByBaby.value[id] || []) : [];
  });

  // Getters de filtrado (restaurados para compatibilidad)
  const feedingEvents = computed(() => events.value.filter(e => e.event_type === "feeding"));
  const sleepEvents = computed(() => events.value.filter(e => e.event_type === "sleep"));
  const diaperEvents = computed(() => events.value.filter(e => e.event_type === "diaper"));

  /**
   * Obtiene el último registro de cada tipo de evento para un bebé específico.
   * Usado en las tarjetas del Dashboard.
   */
  const getLatestEventsByType = (babyId) => {
    const list = eventsByBaby.value[babyId] || [];
    const latest = {};
    
    // Orden descendente por fecha
    const sorted = [...list].sort((a, b) => new Date(b.occurred_at) - new Date(a.occurred_at));
    
    sorted.forEach(event => {
      if (!latest[event.event_type]) {
        latest[event.event_type] = event;
      }
    });
    
    return Object.values(latest).sort((a, b) => new Date(b.occurred_at) - new Date(a.occurred_at));
  };

  async function fetchEvents(babyId, params = {}) {
    if (!babyId) return [];
    
    isLoading.value = true;
    error.value = null;

    try {
      const data = await eventsApi.listEvents(babyId, params);
      eventsByBaby.value[babyId] = data;
      return data;
    } catch (err) {
      error.value = normalizeApiError(err, "Error al cargar eventos");
      throw err;
    } finally {
      isLoading.value = false;
    }
  }

  /**
   * Carga masiva para el Dashboard (optimiza peticiones concurrentes)
   */
  async function fetchEventsForMultipleBabies(babies) {
    if (!babies || babies.length === 0) return;
    
    isLoading.value = true;
    try {
      await Promise.all(
        babies.map(baby => fetchEvents(baby.id, { limit: 15 }))
      );
    } catch (err) {
      console.error("Error en carga agregada de eventos", err);
    } finally {
      isLoading.value = false;
    }
  }

  async function createEvent(babyId, eventData) {
    error.value = null;
    try {
      const newEvent = await eventsApi.createEvent(babyId, eventData);
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
      if (eventsByBaby.value[babyId]) {
        eventsByBaby.value[babyId] = eventsByBaby.value[babyId].filter(e => e.id !== eventId);
      }
    } catch (err) {
      error.value = normalizeApiError(err, "Error al eliminar evento");
      throw err;
    }
  }

  return {
    events,
    eventsByBaby,
    isLoading,
    error,
    feedingEvents,
    sleepEvents,
    diaperEvents,
    getLatestEventsByType,
    fetchEvents,
    fetchEventsForMultipleBabies,
    createEvent,
    updateEvent,
    deleteEvent,
  };
});
