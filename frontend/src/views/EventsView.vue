<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Historial</p>
          <h1 class="mt-3 text-3xl font-bold text-ink">Registro de eventos</h1>
          <p class="mt-2 text-sm text-forest/80">
            Sigue el día a día de tu bebé: alimentación, sueño, pañales y más.
          </p>
        </div>
        <RouterLink v-if="!resolvedBabyId" to="/babies" class="btn-primary">
          Ir a bebés
        </RouterLink>
      </div>

      <!-- No Active Baby State -->
      <div
        v-if="!resolvedBabyId"
        class="rounded-4xl border border-sage bg-white/90 p-8 text-center text-forest/80"
      >
        <p class="text-lg font-semibold">No hay bebé activo</p>
        <p class="mt-3">
          Selecciona un bebé en la pantalla de gestión para empezar a registrar sus eventos.
        </p>
        <RouterLink to="/babies" class="btn-primary mt-6 inline-flex">
          Ver bebés
        </RouterLink>
      </div>

      <!-- Main Content -->
      <div v-else>
        <!-- Loading / Error -->
        <div
          v-if="isBootstrapping || babiesStore.isLoading || eventsStore.isLoading"
          class="rounded-3xl bg-white/90 p-8 text-center shadow-sm"
        >
          <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
        </div>

        <div
          v-else-if="babiesStore.error || eventsStore.error"
          class="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700"
        >
          <p class="font-semibold">Error</p>
          <p class="mt-2">{{ babiesStore.error || eventsStore.error }}</p>
        </div>

        <div v-else>
          <!-- Quick Actions & Baby Summary -->
          <div class="grid gap-6 lg:grid-cols-[1fr_1.5fr]">
            <!-- Baby Summary -->
            <section class="card rounded-4xl p-6 h-fit">
              <p class="section-kicker">Bebé</p>
              <h2 class="mt-2 text-2xl font-semibold text-ink">{{ baby?.name || "Bebé activo" }}</h2>
              <p class="mt-1 text-sm text-forest/75">
                {{ baby ? `Nacido el ${formatDate(baby.birth_date)}` : "" }}
              </p>

              <div class="mt-6 space-y-3">
                 <div class="rounded-3xl border border-sage bg-mist p-4 flex justify-between items-center">
                    <div>
                      <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Edad</p>
                      <p class="mt-1 text-sm text-ink">{{ babyAge }}</p>
                    </div>
                    <div class="h-10 w-10 rounded-full bg-leaf/10 flex items-center justify-center text-leaf">
                      <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                    </div>
                 </div>
              </div>
            </section>

            <!-- Quick Entry -->
            <section class="card rounded-4xl p-6">
              <div class="flex items-center justify-between mb-6">
                <div>
                  <p class="section-kicker">Acción rápida</p>
                  <h2 class="text-2xl font-semibold text-ink">Registrar ahora</h2>
                </div>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-3 gap-4">
                <button 
                  v-for="type in eventTypes" 
                  :key="type.id"
                  @click="openEventModal(type.id)"
                  class="flex flex-col items-center justify-center p-4 rounded-3xl border border-sage bg-white hover:border-leaf hover:bg-leaf/5 transition-all group"
                >
                  <div class="h-12 w-12 rounded-2xl bg-mist flex items-center justify-center text-forest group-hover:bg-leaf/10 group-hover:text-leaf mb-3">
                    <component :is="type.icon" class="h-6 w-6" />
                  </div>
                  <span class="text-sm font-medium text-ink">{{ type.label }}</span>
                </button>
              </div>
            </section>
          </div>

          <!-- History & Filters -->
          <section class="mt-8 rounded-4xl border border-sage bg-white/90 p-6">
            <div class="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between mb-8">
              <div>
                <p class="section-kicker">Cronología</p>
                <h2 class="mt-2 text-2xl font-semibold text-ink">Historial de eventos</h2>
              </div>

              <!-- Filter Tabs -->
              <div class="flex bg-mist p-1 rounded-2xl overflow-x-auto no-scrollbar">
                <button 
                  @click="activeFilter = 'all'"
                  :class="[activeFilter === 'all' ? 'bg-white shadow-sm text-leaf' : 'text-forest/60 hover:text-forest']"
                  class="px-4 py-2 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all whitespace-nowrap"
                >
                  Todos
                </button>
                <button 
                  v-for="type in eventTypes"
                  :key="type.id"
                  @click="activeFilter = type.id"
                  :class="[activeFilter === type.id ? 'bg-white shadow-sm text-leaf' : 'text-forest/60 hover:text-forest']"
                  class="px-4 py-2 rounded-xl text-xs font-semibold uppercase tracking-wider transition-all whitespace-nowrap"
                >
                  {{ type.label }}
                </button>
              </div>
            </div>

            <!-- Events List -->
            <div v-if="filteredEvents.length === 0" class="py-12 text-center">
              <div class="h-16 w-16 bg-mist rounded-full flex items-center justify-center mx-auto text-forest/30 mb-4">
                <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <p class="text-forest/75 font-medium">No se encontraron eventos</p>
              <p class="text-sm text-forest/50 mt-1">Usa los botones de arriba para registrar el primero.</p>
            </div>

            <div v-else class="space-y-4">
              <article 
                v-for="event in filteredEvents" 
                :key="event.id"
                class="group relative flex items-start gap-4 p-5 rounded-3xl border border-sage bg-white hover:shadow-md transition-all"
              >
                <!-- Icon -->
                <div :class="getTypeColor(event.event_type)" class="flex-shrink-0 h-12 w-12 rounded-2xl flex items-center justify-center">
                  <component :is="getTypeIcon(event.event_type)" class="h-6 w-6" />
                </div>

                <!-- Info -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-center justify-between mb-1">
                    <h3 class="font-semibold text-ink text-sm">
                      {{ getEventLabel(event.event_type) }}
                      <span v-if="event.amount" class="text-forest/60 font-normal ml-1">
                        ({{ event.amount }} ml/min)
                      </span>
                    </h3>
                    <time class="text-[10px] uppercase tracking-wider text-forest/40 font-bold">
                      {{ formatTime(event.occurred_at) }}
                    </time>
                  </div>
                  <p class="text-sm text-forest/75 line-clamp-2">
                    {{ event.notes || getDefaultNote(event.event_type) }}
                  </p>
                  <p class="mt-2 text-[11px] text-forest/40">
                    {{ formatDate(event.occurred_at) }}
                  </p>
                </div>

                <!-- Actions (Hover) -->
                <div class="absolute top-4 right-4 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button @click="editEvent(event)" class="p-2 text-forest/60 hover:text-leaf hover:bg-leaf/10 rounded-lg transition-colors">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button @click="confirmDeleteEvent(event)" class="p-2 text-forest/60 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </article>
            </div>
          </section>
        </div>
      </div>
    </div>

    <!-- Event Modal Form -->
    <div v-if="showEventForm" class="fixed inset-0 z-50 bg-slate-900/40 px-4 py-6 flex items-center justify-center">
      <div class="w-full max-w-lg rounded-3xl bg-white p-6 shadow-2xl animate-in fade-in zoom-in duration-200">
        <div class="flex items-start justify-between mb-6">
          <div class="flex items-center gap-3">
             <div :class="getTypeColor(eventForm.event_type)" class="h-10 w-10 rounded-xl flex items-center justify-center">
                <component :is="getTypeIcon(eventForm.event_type)" class="h-5 w-5" />
             </div>
             <div>
                <p class="section-kicker">{{ editingEvent ? 'Editar' : 'Nuevo' }}</p>
                <h2 class="text-xl font-bold text-ink">{{ getEventLabel(eventForm.event_type) }}</h2>
             </div>
          </div>
          <button @click="closeEventModal" class="text-forest/40 hover:text-ink transition-colors">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveEvent" class="space-y-4">
          <div>
            <label class="label">Fecha y hora</label>
            <input v-model="eventForm.occurred_at" type="datetime-local" class="input" required />
          </div>

          <div v-if="['feeding', 'sleep'].includes(eventForm.event_type)">
            <label class="label">
              {{ eventForm.event_type === 'feeding' ? 'Cantidad (ml)' : 'Duración (min)' }}
            </label>
            <input 
              v-model.number="eventForm.amount" 
              type="number" 
              min="0"
              class="input" 
              placeholder="Ej: 120"
            />
          </div>

          <div>
            <label class="label">Notas / Observaciones</label>
            <textarea 
              v-model="eventForm.notes" 
              rows="3" 
              class="input" 
              placeholder="Opcional..."
            ></textarea>
          </div>

          <div class="pt-4 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button type="button" class="btn-muted" @click="closeEventModal">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSavingEvent">
              {{ isSavingEvent ? 'Guardando...' : (editingEvent ? 'Actualizar' : 'Registrar') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted, markRaw } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useBabiesStore } from "../stores/babies";
import { useEventsStore } from "../stores/events";
import { useToast } from "../composables/toast";

// Icons (using inline SVGs for simplicity and avoiding dependency issues)
const IconFeeding = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M3 12H2m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>' };
const IconSleep = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>' };
const IconDiaper = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>' };
const IconBath = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>' };
const IconMed = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" /></svg>' };
const IconNote = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>' };

const route = useRoute();
const authStore = useAuthStore();
const babiesStore = useBabiesStore();
const eventsStore = useEventsStore();
const toast = useToast();

const isBootstrapping = ref(false);
const showEventForm = ref(false);
const isSavingEvent = ref(false);
const editingEvent = ref(null);
const activeFilter = ref('all');

const eventTypes = [
  { id: 'feeding', label: 'Alimentación', icon: markRaw(IconFeeding), color: 'bg-amber-100 text-amber-700' },
  { id: 'sleep', label: 'Sueño', icon: markRaw(IconSleep), color: 'bg-indigo-100 text-indigo-700' },
  { id: 'diaper', label: 'Pañal', icon: markRaw(IconDiaper), color: 'bg-emerald-100 text-emerald-700' },
  { id: 'medication', label: 'Medicina', icon: markRaw(IconMed), color: 'bg-red-100 text-red-700' },
  { id: 'bath', label: 'Baño', icon: markRaw(IconBath), color: 'bg-cyan-100 text-cyan-700' },
  { id: 'note', label: 'Nota', icon: markRaw(IconNote), color: 'bg-slate-100 text-slate-700' },
];

const eventForm = reactive({
  event_type: 'feeding',
  occurred_at: '',
  amount: null,
  notes: '',
});

const resolvedBabyId = computed(() => {
  return route.query.babyId || authStore.user?.active_baby_id || babiesStore.activeBabyId || null;
});

const baby = computed(() => babiesStore.baby);

const filteredEvents = computed(() => {
  const allEvents = eventsStore.events || [];
  if (activeFilter.value === 'all') return allEvents;
  return allEvents.filter(e => e.event_type === activeFilter.value);
});

// Helpers
const formatDate = (val) => val ? new Date(val).toLocaleDateString('es-ES', { day: '2-digit', month: 'long', year: 'numeric' }) : '';
const formatTime = (val) => val ? new Date(val).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }) : '';

const babyAge = computed(() => {
  if (!baby.value?.birth_date) return "Edad desconocida";
  const birth = new Date(baby.value.birth_date);
  const today = new Date();
  const diffTime = Math.abs(today - birth);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays < 30) return `${diffDays} días`;
  const diffMonths = Math.floor(diffDays / 30.44);
  if (diffMonths < 12) return `${diffMonths} meses`;
  const diffYears = Math.floor(diffMonths / 12);
  const remMonths = diffMonths % 12;
  return `${diffYears} año${diffYears > 1 ? 's' : ''}${remMonths ? ` y ${remMonths} m` : ''}`;
});

function getTypeIcon(type) {
  return eventTypes.find(t => t.id === type)?.icon || IconNote;
}

function getTypeColor(type) {
  return eventTypes.find(t => t.id === type)?.color || 'bg-mist text-forest';
}

function getEventLabel(type) {
  return eventTypes.find(t => t.id === type)?.label || 'Evento';
}

function getDefaultNote(type) {
  const notes = {
    feeding: 'Toma de leche finalizada.',
    sleep: 'Bebé durmiendo tranquilamente.',
    diaper: 'Cambio de pañal realizado.',
    bath: 'Baño relajante completado.',
    medication: 'Dosis administrada según indicación.',
    note: 'Registro manual.'
  };
  return notes[type] || '';
}

// Actions
function openEventModal(type = 'feeding') {
  editingEvent.value = null;
  eventForm.event_type = type;
  // Set current time in ISO format for datetime-local
  const now = new Date();
  now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
  eventForm.occurred_at = now.toISOString().slice(0, 16);
  eventForm.amount = null;
  eventForm.notes = '';
  showEventForm.value = true;
}

function closeEventModal() {
  showEventForm.value = false;
  editingEvent.value = null;
}

function editEvent(event) {
  editingEvent.value = event;
  eventForm.event_type = event.event_type;
  eventForm.occurred_at = event.occurred_at.slice(0, 16);
  eventForm.amount = event.amount;
  eventForm.notes = event.notes || '';
  showEventForm.value = true;
}

async function saveEvent() {
  if (!resolvedBabyId.value) return;
  isSavingEvent.value = true;
  try {
    const payload = { ...eventForm };
    if (!payload.amount) delete payload.amount;

    if (editingEvent.value) {
      await eventsStore.updateEvent(resolvedBabyId.value, editingEvent.value.id, payload);
      toast.success("Evento actualizado", "El registro se ha actualizado correctamente.");
    } else {
      await eventsStore.createEvent(resolvedBabyId.value, payload);
      toast.success("Evento registrado", "Se ha guardado el evento correctamente.");
    }
    closeEventModal();
  } catch (error) {
    toast.error("Error", eventsStore.error || "No se pudo guardar el evento.");
  } finally {
    isSavingEvent.value = false;
  }
}

async function confirmDeleteEvent(event) {
  const accepted = window.confirm(`¿Eliminar este registro de ${getEventLabel(event.event_type)}?`);
  if (!accepted) return;
  try {
    await eventsStore.deleteEvent(resolvedBabyId.value, event.id);
    toast.success("Evento eliminado", "El registro ha sido borrado.");
  } catch (error) {
    toast.error("Error", "No se pudo eliminar el evento.");
  }
}

async function hydrateContext() {
  isBootstrapping.value = true;
  try {
    await authStore.fetchCurrentUser();
    const babyId = resolvedBabyId.value;
    if (babyId) {
      await Promise.all([
        babiesStore.fetchBaby(babyId),
        eventsStore.fetchEvents(babyId)
      ]);
    }
  } finally {
    isBootstrapping.value = false;
  }
}

watch(resolvedBabyId, async (id) => {
  if (id) {
    await Promise.all([
      babiesStore.fetchBaby(id),
      eventsStore.fetchEvents(id)
    ]);
  }
});

onMounted(hydrateContext);
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
