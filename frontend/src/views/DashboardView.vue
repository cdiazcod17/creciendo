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

      <div class="mb-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <RouterLink
        to="/eventos"
        class="card flex flex-col items-start rounded-3xl border border-sage bg-white/90 p-5 transition-all hover:shadow-md"
        >
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-leaf/10">
            <svg class="h-5 w-5 text-leaf" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <p class="mt-3 text-xs uppercase tracking-[0.18em] text-forest/50">Registro</p>
          <p class="mt-1 text-sm font-semibold text-ink">Eventos</p>
          <p class="mt-1 text-xs text-forest/75">Sueño, alimento, baño</p>
        </RouterLink>
        <RouterLink
          to="/crecimiento"
          class="card flex flex-col items-start rounded-3xl border border-sage bg-white/90 p-5 transition-all hover:shadow-md"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-leaf/10">
            <svg class="h-5 w-5 text-leaf" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          </div>
          <p class="mt-3 text-xs uppercase tracking-[0.18em] text-forest/50">Métricas</p>
          <p class="mt-1 text-sm font-semibold text-ink">Crecimiento</p>
          <p class="mt-1 text-xs text-forest/75">Peso, talla, tipo de sangre (RH)</p>
        </RouterLink>
        
        <RouterLink
          to="/citas"
          class="card flex flex-col items-start rounded-3xl border border-sage bg-white/90 p-5 transition-all hover:shadow-md"
        >
        <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-leaf/10">
            <svg class="h-5 w-5 text-leaf" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <p class="mt-3 text-xs uppercase tracking-[0.18em] text-forest/50">Agenda</p>
          <p class="mt-1 text-sm font-semibold text-ink">Citas</p>
          <p class="mt-1 text-xs text-forest/75">Controles médicos</p>
        </RouterLink>
        
        <RouterLink
          to="/dashboard#babies"
          class="card flex flex-col items-start rounded-3xl border border-sage bg-white/90 p-5 transition-all hover:shadow-md"
        >
          <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-leaf/10">
            <svg class="h-5 w-5 text-leaf" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
            </svg>
          </div>
          <p class="mt-3 text-xs uppercase tracking-[0.18em] text-forest/50">Gestión</p>
          <p class="mt-1 text-sm font-semibold text-ink">Bebés</p>
          <p class="mt-1 text-xs text-forest/75">Ver y editar perfiles</p>
        </RouterLink>

      </div>

      <section class="mb-10" id="babies">
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
          <button
            type="button"
            class="mt-4 text-sm font-medium text-red-600 hover:text-red-500"
            @click="babiesStore.fetchBabies()"
          >
            Reintentar
          </button>
        </div>

        <div v-else-if="!babiesStore.babies.length" class="rounded-4xl border border-sage bg-white/90 p-12 text-center">
          <div class="inline-flex h-16 w-16 items-center justify-center rounded-full bg-mist">
            <svg class="h-8 w-8 text-forest" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
            </svg>
          </div>
          <h3 class="mt-4 text-lg font-semibold text-ink">No hay bebés registrados</h3>
          <p class="mt-2 text-sm text-forest/75">
            Comienza registrando tu primer bebé para acceder a todas las funciones.
          </p>
          <button type="button" class="btn-primary mt-6" @click="showAddBabyModal = true">
            Agregar primer bebé
          </button>
        </div>

        <div v-else class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="baby in babiesStore.babies"
            :key="baby.id"
            class="card rounded-3xl border border-sage bg-white/90 p-6"
          >
            <div class="flex items-center gap-4">
              <button
                v-if="baby.photo_url"
                type="button"
                class="h-16 w-16 overflow-hidden rounded-full bg-mist transition hover:scale-[1.02] focus:outline-none focus:ring-2 focus:ring-leaf"
                @click="openPhotoModal(baby)"
                :aria-label="`Ver foto de ${baby.name}`"
              >
                <img
                  :src="baby.photo_url"
                  :alt="baby.name"
                  class="h-full w-full object-cover"
                />
              </button>

              <div
                v-else
                class="flex h-16 w-16 items-center justify-center rounded-full bg-mist text-forest"
              >
                <svg class="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
                </svg>
              </div>

              <div class="flex-1">
                <p class="text-sm uppercase tracking-[0.18em] text-forest/60">
                  {{ getAge(baby.birth_date) }}
                </p>
                <h3 class="text-xl font-semibold text-ink">{{ baby.name }}</h3>
                <p class="text-xs text-forest/75">{{ formatDate(baby.birth_date) }}</p>
              </div>
            </div>

            <div v-if="baby.notes" class="mt-4 rounded-xl border border-sage bg-mist p-3">
              <p class="text-xs text-forest/75 line-clamp-2">{{ baby.notes }}</p>
            </div>

            <div class="mt-5 flex flex-wrap gap-2">
              <RouterLink
                :to="{ name: 'baby-details', params: { babyId: baby.id } }"
                class="btn-muted flex-1 text-center"
              >
                Editar datos
              </RouterLink>

              <RouterLink
                :to="{ name: 'baby', params: { babyId: baby.id } }"
                class="btn-primary flex-1 bg-leaf text-center hover:bg-forest"
              >
                Seleccionar
              </RouterLink>

              <button
                type="button"
                class="btn-muted flex-1 border-red-200 text-red-600 hover:bg-red-50"
                @click="confirmDelete(baby.id, baby.name)"
              >
                Eliminar
              </button>
            </div>
          </article>
        </div>
      </section>
    </div>

    <div v-if="showAddBabyModal" class="fixed inset-0 z-50 bg-slate-900/40 px-4 py-6">
      <div class="mx-auto max-w-2xl rounded-4xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="section-kicker">Nuevo bebé</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">Registra un nuevo perfil</h2>
          </div>
          <button
            type="button"
            class="text-forest hover:text-ink"
            @click="showAddBabyModal = false"
          >
            ✕
          </button>
        </div>

        <form class="mt-6 space-y-4" @submit.prevent="handleAddBaby">
          <div>
            <label class="label">Nombre</label>
            <input
              v-model="newBaby.name"
              type="text"
              class="input"
              required
              placeholder="Nombre del bebé"
            />
          </div>

          <div>
            <label class="label">Fecha de nacimiento</label>
            <input
              v-model="newBaby.birth_date"
              type="date"
              class="input"
              required
            />
          </div>

          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label class="label">Sexo</label>
              <select v-model="newBaby.sex" class="input">
                <option value="">Seleccionar</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
                <option value="other">Otro</option>
              </select>
            </div>
          </div>

          <div>
            <label class="label">Foto (URL)</label>
            <input
              v-model="newBaby.photo_url"
              type="url"
              class="input"
              placeholder="https://ejemplo.com/foto.jpg"
            />
          </div>

          <div>
            <label class="label">Notas</label>
            <textarea
              v-model="newBaby.notes"
              rows="3"
              class="input"
              placeholder="Observaciones especiales"
            ></textarea>
          </div>

          <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="btn-muted"
              @click="showAddBabyModal = false"
            >
              Cancelar
            </button>
            <button
              type="submit"
              class="btn-primary"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Guardando...' : 'Guardar' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div
      v-if="showPhotoModal && selectedBabyPhoto"
      class="fixed inset-0 z-[60] bg-slate-950/70 px-4 py-6"
      @click.self="closePhotoModal"
    >
      <div class="mx-auto max-w-3xl rounded-4xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="section-kicker">Foto del bebé</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">
              {{ selectedBabyPhoto.name }}
            </h2>
          </div>

          <button
            type="button"
            class="text-forest hover:text-ink"
            @click="closePhotoModal"
          >
            ✕
          </button>
        </div>

        <div class="mt-6 overflow-hidden rounded-3xl bg-mist">
          <img
            :src="selectedBabyPhoto.photo_url"
            :alt="`Foto de ${selectedBabyPhoto.name}`"
            class="h-auto w-full object-cover"
          />
        </div>

        <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
          <button
            type="button"
            class="btn-muted"
            @click="closePhotoModal"
          >
            Cerrar
          </button>
          <button
            type="button"
            class="btn-primary"
            @click="closePhotoModal"
          >
            Guardar
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBabiesStore } from '../stores/babies'
import { useToast } from '../composables/toast'

const babiesStore = useBabiesStore()
const toast = useToast()

const showAddBabyModal = ref(false)
const showPhotoModal = ref(false)
const selectedBabyPhoto = ref(null)
const isSubmitting = ref(false)

const newBaby = ref({
  name: '',
  birth_date: '',
  sex: '',
  notes: '',
  photo_url: '',
})

onMounted(() => {
  babiesStore.fetchBabies()
})

function openPhotoModal(baby) {
  selectedBabyPhoto.value = baby
  showPhotoModal.value = true
}

function closePhotoModal() {
  showPhotoModal.value = false
  selectedBabyPhoto.value = null
}

function getAge(birthDate) {
  const today = new Date()
  const birth = new Date(birthDate)
  const ageInMs = today - birth

  const years = Math.floor(ageInMs / (1000 * 60 * 60 * 24 * 365.25))
  const months = Math.floor((ageInMs % (1000 * 60 * 60 * 24 * 365.25)) / (1000 * 60 * 60 * 24 * 30.44))

  if (years > 0) {
    return `${years} año${years > 1 ? 's' : ''}${months > 0 ? ` ${months} mes${months > 1 ? 'es' : ''}` : ''}`
  } else if (months > 0) {
    return `${months} mes${months > 1 ? 'es' : ''}`
  } else {
    const days = Math.floor(ageInMs / (1000 * 60 * 60 * 24))
    return `${days} día${days > 1 ? 's' : ''}`
  }
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

async function handleAddBaby() {
  isSubmitting.value = true
  try {
    await babiesStore.createBaby(newBaby.value)
    toast.success('Bebé agregado', 'El perfil fue creado correctamente.')
    showAddBabyModal.value = false
    newBaby.value = {
      name: '',
      birth_date: '',
      sex: '',
      notes: '',
      photo_url: '',
    }
  } catch (error) {
    toast.error('Error', babiesStore.error || 'No se pudo crear el bebé.')
  } finally {
    isSubmitting.value = false
  }
}

async function confirmDelete(babyId, babyName) {
  const accepted = window.confirm(`¿Estás seguro de que deseas eliminar el perfil de ${babyName}? Esta acción no se puede deshacer.`)
  if (!accepted) return

  try {
    await babiesStore.deleteBaby(babyId)
    toast.success('Bebé eliminado', 'El perfil fue eliminado correctamente.')
  } catch (error) {
    toast.error('Error', babiesStore.error || 'No se pudo eliminar el bebé.')
  }
}
</script>