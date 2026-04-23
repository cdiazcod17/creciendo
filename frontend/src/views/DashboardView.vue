<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-kicker">Bienvenido</p>
        <h1 class="mt-3 text-4xl font-bold text-ink">Dashboard</h1>
        <p class="mt-2 text-sm text-forest/80">
          Resumen de bebés y acceso rápido a funciones principales.
        </p>
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
          <p class="mt-3 text-[10px] uppercase tracking-[0.18em] text-forest/50 font-bold">{{ link.kicker }}</p>
          <p class="mt-1 text-sm font-semibold text-ink">{{ link.label }}</p>
        </RouterLink>
      </div>

      <!-- Sección de Bebés -->
      <section class="mb-10">
        <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="section-kicker">Perfiles activos</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">Tus bebés</h2>
          </div>

          <button type="button" class="btn-primary" @click="showAddBabyModal = true">
            Agregar bebé
          </button>
        </div>

        <div v-if="babiesStore.isLoading" class="rounded-4xl bg-white/90 p-8 text-center shadow-sm">
          <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
        </div>

        <div v-else-if="babiesStore.error" class="rounded-4xl border border-red-200 bg-red-50 p-6 text-red-700">
          <p class="font-semibold">Error al cargar</p>
          <p class="mt-2 text-sm">{{ babiesStore.error }}</p>
          <button type="button" class="mt-4 text-sm font-medium text-red-600 hover:text-red-500" @click="initializeDashboard">
            Reintentar
          </button>
        </div>

        <!-- Empty State -->
        <div v-else-if="!babiesStore.babies.length" class="rounded-4xl border border-sage bg-white/90 p-12 text-center">
          <div class="inline-flex h-16 w-16 items-center justify-center rounded-full bg-mist text-forest">
             <svg class="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4zM6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" /></svg>
          </div>
          <h3 class="mt-4 text-lg font-semibold text-ink">No hay bebés registrados</h3>
          <p class="mt-2 text-sm text-forest/75">Comienza registrando tu primer bebé.</p>
          <button type="button" class="btn-primary mt-6" @click="showAddBabyModal = true">Agregar primer bebé</button>
        </div>

        <!-- Grid de Bebés -->
        <div v-else class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="baby in babiesStore.babies"
            :key="baby.id"
            :class="[
              'card flex flex-col rounded-3xl border p-5 transition-all duration-300',
              isBabySelected(baby.id)
                ? 'border-leaf bg-leaf/5 ring-2 ring-leaf/30 shadow-lg scale-[1.02]'
                : 'border-sage bg-white/90 hover:shadow-md'
            ]"
          >
            <!-- Cabecera de la Tarjeta -->
            <div class="flex items-center gap-4">
              <div class="h-14 w-14 flex-shrink-0 overflow-hidden rounded-full border border-sage/50 bg-mist">
                <img v-if="baby.photo_url" :src="baby.photo_url" :alt="baby.name" class="h-full w-full object-cover" />
                <div v-else class="flex h-full w-full items-center justify-center text-forest/40">
                  <svg class="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
                </div>
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <p class="text-[10px] uppercase tracking-widest text-forest/60 font-bold truncate">
                    {{ getAge(baby.birth_date) }}
                  </p>
                  <span v-if="isBabySelected(baby.id)" class="inline-flex items-center rounded-full bg-leaf px-2 py-0.5 text-[9px] font-bold uppercase tracking-widest text-white">
                    Activo
                  </span>
                </div>
                <h3 class="text-lg font-bold text-ink truncate">{{ baby.name }}</h3>
                <p class="text-xs text-forest/60">{{ formatDate(baby.birth_date) }}</p>
              </div>
            </div>

            <!-- EVENTOS RECIENTES (Último por tipo) -->
            <div class="mt-5 flex-1 space-y-3">
              <div class="flex items-center justify-between border-b border-sage/30 pb-1">
                <span class="text-[10px] font-bold uppercase tracking-[0.18em] text-forest/40">Últimos registros</span>
                <RouterLink :to="{ name: 'eventos', query: { babyId: baby.id } }" class="text-[10px] font-bold text-leaf hover:underline">Ver todo</RouterLink>
              </div>

              <div v-if="eventsStore.getLatestEventsByType(baby.id).length > 0" class="space-y-2.5">
                <div 
                  v-for="event in eventsStore.getLatestEventsByType(baby.id)" 
                  :key="event.id"
                  class="flex items-start gap-2.5"
                >
                  <div :class="getEventTypeStyles(event.event_type)" class="p-1 rounded-lg mt-0.5 flex-shrink-0">
                    <component :is="getEventIcon(event.event_type)" class="h-4 w-4" />
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="flex justify-between gap-2">
                      <span class="font-bold text-ink text-xs truncate">{{ getEventLabel(event.event_type) }}</span>
                      <span class="text-[9px] text-forest/40 whitespace-nowrap font-medium">{{ formatTime(event.occurred_at) }}</span>
                    </div>
                    <p v-if="event.notes" class="text-forest/60 line-clamp-1 text-[11px] leading-tight">{{ event.notes }}</p>
                  </div>
                </div>
              </div>
              <p v-else class="py-3 text-center text-[11px] text-forest/40 italic">Sin eventos registrados</p>
            </div>

            <!-- Acciones -->
            <div class="mt-6 flex gap-2">
              <RouterLink :to="{ name: 'baby-details', params: { babyId: baby.id } }" class="btn-muted flex-1 text-[11px] py-2 font-bold">Perfil</RouterLink>
              <button
                type="button"
                :disabled="isSelectingBaby || isBabySelected(baby.id)"
                :class="[
                  'flex-[1.5] text-[11px] font-bold transition-all py-2 rounded-xl border',
                  isBabySelected(baby.id)
                    ? 'bg-slate-50 text-slate-400 border-transparent cursor-not-allowed'
                    : 'bg-leaf text-white border-leaf hover:bg-forest'
                ]"
                @click="handleSelectBaby(baby)"
              >
                {{ isBabySelected(baby.id) ? 'Seleccionado' : 'Seleccionar' }}
              </button>
              <button type="button" class="px-2.5 rounded-xl border border-red-100 text-red-400 hover:bg-red-50 transition-colors" @click="confirmDelete(baby.id, baby.name)">
                <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </div>
          </article>
        </div>
      </section>
    </div>

    <!-- Modal para Agregar Bebé -->
    <div v-if="showAddBabyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4">
      <div class="w-full max-w-lg rounded-4xl bg-white p-8 shadow-2xl">
        <h2 class="text-2xl font-bold text-ink">Nuevo Bebé</h2>
        <form class="mt-6 space-y-4" @submit.prevent="handleAddBaby">
          <div><label class="label">Nombre</label><input v-model="newBaby.name" type="text" class="input" required placeholder="Nombre del bebé" /></div>
          <div><label class="label">Fecha de nacimiento</label><input v-model="newBaby.birth_date" type="date" class="input" required /></div>
          <div class="flex gap-4 pt-4">
             <button type="button" class="btn-muted flex-1" @click="showAddBabyModal = false">Cancelar</button>
             <button type="submit" class="btn-primary flex-1" :disabled="isSubmitting">{{ isSubmitting ? 'Guardando...' : 'Crear perfil' }}</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, markRaw } from 'vue'
import { useBabiesStore } from '../stores/babies'
import { useAuthStore } from '../stores/auth'
import { useEventsStore } from '../stores/events'
import { useToast } from '../composables/toast'

const babiesStore = useBabiesStore()
const authStore = useAuthStore()
const eventsStore = useEventsStore()
const toast = useToast()

const showAddBabyModal = ref(false)
const isSubmitting = ref(false)
const isSelectingBaby = ref(false)
const pendingBabyId = ref(null)

const newBaby = ref({ name: '', birth_date: '', sex: 'other', notes: '', photo_url: '' })

// Componentes de iconos inline
const IconFeeding = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M3 12H2m15.364 6.364l-.707-.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>' };
const IconSleep = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>' };
const IconDiaper = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>' };
const IconGeneric = { template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>' };

const quickLinks = [
  { name: 'babies', to: '/babies', kicker: 'Perfiles', label: 'Bebés', icon: markRaw(IconGeneric) },
  { name: 'appointments', to: '/appointments', kicker: 'Agenda', label: 'Citas', icon: markRaw({ template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>' }) },
  { name: 'eventos', to: '/eventos', kicker: 'Registro', label: 'Eventos', icon: markRaw(IconFeeding) },
  { name: 'growth', to: '/crecimiento', kicker: 'Métricas', label: 'Evolución', icon: markRaw({ template: '<svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>' }) }
];

async function initializeDashboard() {
  await Promise.all([
    babiesStore.fetchBabies(),
    authStore.fetchCurrentUser()
  ]);
  if (babiesStore.babies.length > 0) {
    eventsStore.fetchEventsForMultipleBabies(babiesStore.babies);
  }
}

onMounted(initializeDashboard);

function isBabySelected(babyId) {
  return babiesStore.activeBabyId === babyId;
}

function getAge(birthDate) {
  const diff = new Date() - new Date(birthDate);
  const months = Math.floor(diff / (1000 * 60 * 60 * 24 * 30.44));
  if (months < 1) return 'Recién nacido';
  if (months < 12) return `${months} m`;
  const years = Math.floor(months / 12);
  const rem = months % 12;
  return `${years}a ${rem > 0 ? rem + 'm' : ''}`;
}

const formatDate = (d) => new Date(d).toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
const formatTime = (d) => new Date(d).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });

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
    toast.success('Bebé activo', `${baby.name} es ahora el perfil principal.`);
  } catch (error) {
    toast.error('Error', 'No se pudo cambiar el perfil.');
  } finally {
    isSelectingBaby.value = false;
    pendingBabyId.value = null;
  }
}

async function handleAddBaby() {
  isSubmitting.value = true;
  try {
    await babiesStore.createBaby(newBaby.value);
    toast.success('Bebé creado', 'Perfil registrado con éxito.');
    showAddBabyModal.value = false;
    newBaby.value = { name: '', birth_date: '', sex: 'other', notes: '', photo_url: '' };
    await initializeDashboard();
  } catch (error) {
    toast.error('Error', babiesStore.error || 'Fallo al crear.');
  } finally {
    isSubmitting.value = false;
  }
}

async function confirmDelete(id, name) {
  if (window.confirm(`¿Estás seguro de que deseas eliminar el perfil de ${name}?`)) {
    try {
      await babiesStore.deleteBaby(id);
      toast.success('Eliminado', 'Perfil borrado correctamente.');
    } catch (e) {
      toast.error('Error', 'No se pudo borrar el perfil.');
    }
  }
}
</script>
