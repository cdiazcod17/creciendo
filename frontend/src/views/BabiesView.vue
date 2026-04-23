<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-kicker">Gestión</p>
        <h1 class="mt-3 text-4xl font-bold text-ink">Mis Bebés</h1>
        <p class="mt-2 text-sm text-forest/80">
          Administra los perfiles de tus bebés y selecciona cuál está activo.
        </p>
      </div>

      <!-- Loading State -->
      <div v-if="babiesStore.isLoading" class="flex justify-center py-12">
        <div class="h-8 w-8 animate-spin rounded-full border-4 border-leaf border-t-transparent"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="babiesStore.error" class="rounded-2xl bg-red-50 p-6 text-center">
        <svg class="mx-auto h-12 w-12 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
        </svg>
        <h3 class="mt-4 text-lg font-semibold text-red-800">Error al cargar bebés</h3>
        <p class="mt-2 text-sm text-red-700">{{ babiesStore.error }}</p>
        <button
          @click="fetchBabies"
          class="mt-4 rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
        >
          Reintentar
        </button>
      </div>

      <!-- Vacio State -->
      <div v-else-if="!babiesStore.hasBabies" class="text-center py-12">
        <svg class="mx-auto h-24 w-24 text-forest/30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
        </svg>
        <h3 class="mt-6 text-xl font-semibold text-ink">No tienes bebés registrados</h3>
        <p class="mt-2 text-sm text-forest/75">Comienza agregando el perfil de tu primer bebé.</p>
        <RouterLink
          to="/babies/new"
          class="mt-6 inline-flex items-center rounded-lg bg-leaf px-4 py-2 text-sm font-medium text-white hover:bg-leaf/90"
        >
          <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Agregar primer bebé
        </RouterLink>
      </div>

      <!-- Babies -->
      <div v-else class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div
          v-for="baby in babiesStore.babies"
          :key="baby.id"
          class="group relative overflow-hidden rounded-3xl border border-sage bg-white/90 p-6 transition-all hover:shadow-lg"
          :class="{ 'ring-2 ring-leaf': baby.id === babiesStore.activeBabyId }"
        >
          <!-- Active -->
          <div
            v-if="baby.id === babiesStore.activeBabyId"
            class="absolute right-4 top-4 rounded-full bg-leaf px-2 py-1 text-xs font-medium text-white"
          >
            Activo
          </div>
         
          <div class="flex items-center justify-center">
            <div class="h-20 w-20 overflow-hidden rounded-full bg-leaf/10">
              <img
                v-if="baby.photo_url"
                :src="baby.photo_url"
                :alt="baby.name"
                class="h-full w-full object-cover"
              />
              <div v-else class="flex h-full w-full items-center justify-center">
                <svg class="h-8 w-8 text-leaf/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
          </div>
          
          <div class="mt-4 text-center">
            <h3 class="text-lg font-semibold text-ink">{{ baby.name }}</h3>
            <p class="text-sm text-forest/75">
              {{ formatDate(baby.birth_date) }} • {{ baby.sex === 'M' ? 'Masculino' : baby.sex === 'F' ? 'Femenino' : 'No especificado' }}
            </p>
            <p v-if="baby.notes" class="mt-2 text-xs text-forest/60 line-clamp-2">
              {{ baby.notes }}
            </p>
          </div>
          
          <div class="mt-6 flex gap-2">
            <button
              v-if="baby.id !== babiesStore.activeBabyId"
              @click="setActiveBaby(baby.id)"
              class="flex-1 rounded-lg bg-leaf/10 px-3 py-2 text-sm font-medium text-leaf hover:bg-leaf/20"
            >
              Activar
            </button>
            <RouterLink
              :to="`/babies/${baby.id}`"
              class="flex-1 rounded-lg bg-forest/10 px-3 py-2 text-center text-sm font-medium text-forest hover:bg-forest/20"
            >
              Editar
            </RouterLink>
          </div>
        </div>
        
        <RouterLink
          to="/babies/new"
          class="group flex flex-col items-center justify-center rounded-3xl border-2 border-dashed border-sage bg-white/50 p-6 transition-all hover:bg-white/90 hover:shadow-lg"
        >
          <div class="flex h-16 w-16 items-center justify-center rounded-full bg-leaf/10 group-hover:bg-leaf/20">
            <svg class="h-8 w-8 text-leaf" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
            </svg>
          </div>
          <p class="mt-4 text-sm font-medium text-ink">Agregar bebé</p>
          <p class="mt-1 text-xs text-forest/75">Nuevo perfil</p>
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useBabiesStore } from '../stores/babies'
import { useToast } from '../composables/toast'

const babiesStore = useBabiesStore()
const toast = useToast()

const fetchBabies = async () => {
  try {
    await babiesStore.fetchBabies()
  } catch (error) {
    console.error('Error fetching babies:', error)
  }
}

const setActiveBaby = async (babyId) => {
  try {
    await babiesStore.setActiveBaby(babyId, true)
    toast.success('Bebé activo', 'La selección del bebé ha sido guardada.')
  } catch (error) {
    console.error('Error setting active baby:', error)
    toast.error('Error', 'No se pudo guardar la selección del bebé.')
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchBabies()
})
</script>