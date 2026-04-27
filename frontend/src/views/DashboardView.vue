<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-kicker">Resumen</p>
        <h1 class="mt-3 text-4xl font-bold text-ink">Dashboard</h1>
        <p class="mt-2 text-sm text-forest/80">Gestión de perfiles, próximas citas y rutinas.</p>
      </div>

      <!-- Accesos Rápidos -->
      <div class="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <RouterLink
          v-for="link in quickLinks"
          :key="link.name"
          :to="link.to"
          class="card flex flex-col items-start rounded-3xl border border-sage bg-white/90 p-5 transition-all hover:shadow-md group"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-leaf/10 group-hover:bg-leaf/20 transition-colors">
            <component :is="link.icon" class="h-5 w-5 text-leaf" />
          </div>
          <p class="mt-3 text-[10px] uppercase tracking-[0.2em] text-forest/40 font-bold">{{ link.kicker }}</p>
          <p class="mt-1 text-sm font-semibold text-ink">{{ link.label }}</p>
        </RouterLink>
      </div>

      <!-- Sección de Bebés -->
      <section>
        <div class="mb-6 flex items-center justify-between">
          <h2 class="text-2xl font-semibold text-ink">Tus bebés</h2>
          <button type="button" class="btn-primary py-2 text-xs" @click="showAddBabyModal = true">
            Agregar bebé
          </button>
        </div>

        <div v-if="babiesStore.isLoading" class="flex justify-center py-12">
          <div class="h-10 w-10 animate-spin rounded-full border-b-2 border-leaf"></div>
        </div>

        <div v-else class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="baby in babiesStore.babies"
            :key="baby.id"
            :class="[
              'card flex flex-col rounded-3xl border p-5 transition-all duration-300',
              isBabySelected(baby.id) ? 'border-leaf bg-leaf/5 ring-1 ring-leaf/20 shadow-lg' : 'border-sage bg-white/95'
            ]"
          >
            <!-- Perfil Superior -->
            <div class="flex items-center gap-4">
              <div class="h-14 w-14 flex-shrink-0 overflow-hidden rounded-full border border-sage/50 bg-mist">
                <img v-if="baby.photo_url" :src="baby.photo_url" :alt="baby.name" class="h-full w-full object-cover" />
                <div v-else class="flex h-full w-full items-center justify-center text-forest/30">
                  <svg class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <h3 class="truncate text-lg font-bold text-ink">{{ baby.name }}</h3>
                <p class="text-[10px] font-bold uppercase tracking-widest text-forest/50">
                  {{ getAge(baby.birth_date) }} • {{ formatDate(baby.birth_date) }}
                </p>
              </div>
            </div>

            <!-- PRÓXIMA CITA -->
            <div class="mt-5 rounded-2xl border border-leaf/20 bg-leaf/5 p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-bold uppercase tracking-[0.15em] text-leaf">Próxima cita</span>
                <RouterLink :to="{ name: 'appointments', query: { babyId: baby.id } }" class="text-[9px] font-bold text-leaf hover:underline uppercase tracking-wider">Agenda</RouterLink>
              </div>

              <div v-if="appointmentsStore.getNextAppointmentByBabyId(baby.id)" class="flex items-center gap-3">
                <div class="h-10 w-10 flex-shrink-0 bg-white rounded-xl border border-leaf/10 flex flex-col items-center justify-center shadow-sm">
                   <span class="text-[10px] font-bold text-leaf leading-none">{{ getAppointmentDay(appointmentsStore.getNextAppointmentByBabyId(baby.id).scheduled_at) }}</span>
                   <span class="text-[9px] font-medium text-forest/40 uppercase leading-none mt-1">{{ getAppointmentMonth(appointmentsStore.getNextAppointmentByBabyId(baby.id).scheduled_at) }}</span>
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-xs font-bold text-ink truncate">{{ appointmentsStore.getNextAppointmentByBabyId(baby.id).title }}</p>
                  <p class="text-[11px] text-forest/60 mt-0.5">
                    {{ formatTime(appointmentsStore.getNextAppointmentByBabyId(baby.id).scheduled_at) }} 
                    <span v-if="appointmentsStore.getNextAppointmentByBabyId(baby.id).provider_name" class="mx-1 opacity-50">•</span>
                    {{ appointmentsStore.getNextAppointmentByBabyId(baby.id).provider_name }}
                  </p>
                </div>
              </div>
              <div v-else class="text-center py-1">
                <p class="text-[11px] font-medium text-forest/40 italic">Sin citas próximas</p>
              </div>
            </div>


            <div class="mt-5 flex-1">
              <div class="flex items-center justify-between mb-2 pb-1 border-b border-sage/30">
                <span class="text-[10px] font-bold uppercase tracking-[0.15em] text-forest/40">Últimas rutinas</span>
                <RouterLink :to="{ name: 'eventos', query: { babyId: baby.id } }" class="text-[10px] font-bold text-forest/40 hover:text-leaf transition-colors">Historial</RouterLink>
              </div>

              <div v-if="eventsStore.getLatestEventsByType(baby.id).length > 0" class="space-y-2">
                <div 
                  v-for="event in eventsStore.getLatestEventsByType(baby.id)" 
                  :key="event.id"
                  class="flex items-start gap-3"
                >
                  <div :class="getEventTypeStyles(event.event_type)" class="mt-0.5 flex h-6 w-6 flex-shrink-0 items-center justify-center rounded-lg">
                    <component :is="getEventIcon(event.event_type)" class="h-3.5 w-3.5" />
                  </div>
                  <div class="min-w-0 flex-1">
                    <div class="flex items-center justify-between gap-2">
                      <span class="truncate text-[13px] font-bold text-ink">{{ getEventLabel(event.event_type) }}</span>
                      <span class="whitespace-nowrap text-[10px] font-semibold text-forest/30 uppercase">{{ formatTime(event.occurred_at) }}</span>
                    </div>
                    <p v-if="event.notes" class="mt-0.5 line-clamp-1 text-xs leading-tight text-forest/60">
                      {{ event.notes }}
                    </p>
                  </div>
                </div>
              </div>
              <div v-else class="py-2 text-center text-[11px] text-forest/30 italic">Sin registros diarios</div>
            </div>


            <div class="mt-6 flex gap-2">
              <RouterLink :to="{ name: 'baby-details', params: { babyId: baby.id } }" class="btn-muted flex-1 py-2 text-xs font-bold">Detalles</RouterLink>
              <button
                type="button"
                :disabled="isSelectingBaby || isBabySelected(baby.id)"
                :class="[
                  'flex-[1.5] rounded-xl text-xs font-bold transition-colors border',
                  isBabySelected(baby.id)
                    ? 'bg-slate-50 text-slate-300 border-slate-100 cursor-not-allowed'
                    : 'bg-leaf text-white border-leaf hover:bg-forest hover:border-forest shadow-sm'
                ]"
                @click="handleSelectBaby(baby)"
              >
                {{ isBabySelected(baby.id) ? 'Activo' : 'Seleccionar' }}
              </button>
              <button type="button" class="px-2.5 rounded-xl border border-red-100 text-red-300 hover:bg-red-50 transition-colors" @click="confirmDelete(baby.id, baby.name)">
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </article>
        </div>
      </section>
    </div>

    <!-- Modal para Agregar Bebé -->
    <div v-if="showAddBabyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4">
      <div class="w-full max-w-md rounded-4xl bg-white p-8 shadow-2xl">
        <h2 class="text-xl font-bold text-ink">Nuevo perfil</h2>
        <form class="mt-4 space-y-4" @submit.prevent="handleAddBaby">
          <div><label class="label">Nombre</label><input v-model="newBaby.name" type="text" class="input" required /></div>
          <div><label class="label">Nacimiento</label><input v-model="newBaby.birth_date" type="date" class="input" required /></div>
          <div class="flex gap-3 pt-2">
             <button type="button" class="btn-muted flex-1" @click="showAddBabyModal = false">Cancelar</button>
             <button type="submit" class="btn-primary flex-1" :disabled="isSubmitting">{{ isSubmitting ? 'Guardando...' : 'Crear' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw, h } from 'vue'
import { useBabiesStore } from '../stores/babies'
import { useAuthStore } from '../stores/auth'
import { useEventsStore } from '../stores/events'
import { useAppointmentsStore } from '../stores/appointments'
import { useToast } from '../composables/toast'

const babiesStore = useBabiesStore()
const authStore = useAuthStore()
const eventsStore = useEventsStore()
const appointmentsStore = useAppointmentsStore()
const toast = useToast()

const showAddBabyModal = ref(false)
const isSubmitting = ref(false)
const isSelectingBaby = ref(false)
const pendingBabyId = ref(null)

const newBaby = ref({ name: '', birth_date: '', sex: 'other', notes: '', photo_url: '' })

// Icons as functional components
const IconFeeding = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 3v1m0 16v1m9-9h-1M3 12H2m15.364 6.364l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z' })
]);
const IconSleep = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z' })
]);
const IconDiaper = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z' })
]);
const IconGeneric = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
]);
const IconAppointment = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' })
]);
const IconGrowth = (props) => h('svg', { ...props, fill: 'none', viewBox: '0 0 24 24', stroke: 'currentColor' }, [
  h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' })
]);

const quickLinks = [
  { name: 'babies', to: '/babies', kicker: 'Perfiles', label: 'Mis Bebés', icon: markRaw(IconGeneric) },
  { name: 'appointments', to: '/appointments', kicker: 'Médico', label: 'Citas', icon: markRaw(IconAppointment) },
  { name: 'eventos', to: '/eventos', kicker: 'Rutina', label: 'Eventos', icon: markRaw(IconFeeding) },
  { name: 'growth', to: '/crecimiento', kicker: 'Evolución', label: 'Crecimiento', icon: markRaw(IconGrowth) }
];

async function initializeDashboard() {
  await Promise.all([babiesStore.fetchBabies(), authStore.fetchCurrentUser()]);
  if (babiesStore.babies.length > 0) {
    // Carga paralela de eventos y citas para todos los bebés
    await Promise.all([
      eventsStore.fetchEventsForMultipleBabies(babiesStore.babies),
      appointmentsStore.fetchAppointmentsForMultipleBabies(babiesStore.babies)
    ]);
  }
}

onMounted(initializeDashboard);

function isBabySelected(babyId) { return babiesStore.activeBabyId === babyId; }

function getAge(birthDate) {
  const diff = new Date() - new Date(birthDate);
  const months = Math.floor(diff / (1000 * 60 * 60 * 24 * 30.44));
  if (months < 1) return 'Recién nacido';
  if (months < 12) return `${months} meses`;
  return `${Math.floor(months / 12)} años`;
}

const formatDate = (d) => new Date(d).toLocaleDateString('es-ES', { day: 'numeric', month: 'short' });
const formatTime = (d) => new Date(d).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
const getAppointmentDay = (d) => new Date(d).getDate();
const getAppointmentMonth = (d) => new Date(d).toLocaleDateString('es-ES', { month: 'short' }).replace('.', '');

function getEventIcon(type) {
  if (type === 'feeding') return IconFeeding;
  if (type === 'sleep') return IconSleep;
  if (type === 'diaper') return IconDiaper;
  return IconGeneric;
}

function getEventTypeStyles(type) {
  const styles = {
    feeding: 'bg-amber-50 text-amber-600 border border-amber-100',
    sleep: 'bg-indigo-50 text-indigo-600 border border-indigo-100',
    diaper: 'bg-emerald-50 text-emerald-600 border border-emerald-100',
    default: 'bg-slate-50 text-slate-500 border border-slate-100'
  };
  return styles[type] || styles.default;
}

function getEventLabel(type) {
  const labels = { feeding: 'Alimentación', sleep: 'Sueño', diaper: 'Pañal', bath: 'Baño', medication: 'Medicina' };
  return labels[type] || 'Evento';
}

async function handleSelectBaby(baby) {
  if (!baby?.id || isBabySelected(baby.id)) return;
  isSelectingBaby.value = true;
  pendingBabyId.value = baby.id;
  try {
    await babiesStore.setActiveBaby(baby.id, true);
    toast.success('Perfil activo', `${baby.name} seleccionado.`);
  } catch (error) {
    toast.error('Error', 'No se pudo activar el perfil.');
  } finally {
    isSelectingBaby.value = false;
    pendingBabyId.value = null;
  }
}

async function handleAddBaby() {
  isSubmitting.value = true;
  try {
    await babiesStore.createBaby(newBaby.value);
    toast.success('Bebé creado', '¡Listo!');
    showAddBabyModal.value = false;
    newBaby.value = { name: '', birth_date: '', sex: 'other', notes: '', photo_url: '' };
    await initializeDashboard();
  } catch (error) {
    toast.error('Error', babiesStore.error || 'No se pudo crear.');
  } finally {
    isSubmitting.value = false;
  }
}

async function confirmDelete(id, name) {
  if (window.confirm(`¿Eliminar perfil de ${name}?`)) {
    try {
      await babiesStore.deleteBaby(id);
      toast.success('Perfil eliminado', 'Correcto.');
    } catch (e) {
      toast.error('Error', 'No se pudo eliminar.');
    }
  }
}
</script>
