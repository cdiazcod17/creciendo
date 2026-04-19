<template>
  <div class="min-h-screen bg-paper py-8">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-ink">Dashboard</h1>
        <p class="mt-2 text-forest">Gestiona tus bebés y su desarrollo</p>
      </div>

      <!-- Loading State -->
      <div v-if="babiesStore.isLoading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-leaf"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="babiesStore.error" class="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">Error al cargar bebés</h3>
            <p class="mt-1 text-sm text-red-700">{{ babiesStore.error }}</p>
            <button
              @click="babiesStore.fetchBabies()"
              class="mt-2 text-sm text-red-600 hover:text-red-500 font-medium"
            >
              Reintentar
            </button>
          </div>
        </div>
      </div>

      <!-- Babies Grid -->
      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Add Baby Card -->
          <div class="bg-white rounded-lg shadow-sm border-2 border-dashed border-sage hover:border-leaf transition-colors duration-200">
            <div class="p-6 text-center">
              <div class="w-16 h-16 mx-auto mb-4 bg-mist rounded-full flex items-center justify-center">
                <svg class="w-8 h-8 text-forest" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
              </div>
              <h3 class="text-lg font-medium text-ink mb-2">Agregar Bebé</h3>
              <p class="text-forest text-sm mb-4">Registra un nuevo bebé para comenzar a monitorear su desarrollo</p>
              <button
                @click="showAddBabyModal = true"
                class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-forest hover:bg-leaf focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Agregar Bebé
              </button>
            </div>
          </div>

          <!-- Baby Cards -->
          <div
            v-for="baby in babiesStore.babies"
            :key="baby.id"
            class="bg-white/90 rounded-lg shadow-sm border border-sage hover:shadow-md transition-shadow duration-200"
          >
            <div class="p-6">
              <!-- Baby Header -->
              <div class="flex items-start justify-between mb-4">
                <div class="flex items-center">
                  <div class="w-12 h-12 bg-mist rounded-full flex items-center justify-center mr-3">
                    <svg class="w-6 h-6 text-forest" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="text-lg font-semibold text-ink">{{ baby.name }}</h3>
                    <p class="text-sm text-forest">{{ getAge(baby.birth_date) }}</p>
                  </div>
                </div>
                <div class="flex space-x-2">
                  <button
                    v-if="babiesStore.activeBabyId !== baby.id"
                    @click="babiesStore.setActiveBaby(baby.id)"
                    class="inline-flex items-center px-3 py-1 border border-sage text-sm font-medium rounded-md text-forest bg-mist hover:bg-mist/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf"
                  >
                    Seleccionar
                  </button>
                  <button
                    v-else
                    class="inline-flex items-center px-3 py-1 border border-forest text-sm font-medium rounded-md text-forest bg-mist cursor-default"
                  >
                    <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                    Activo
                  </button>
                </div>
              </div>

              <!-- Baby Info -->
              <div class="space-y-2">
                <div class="flex items-center text-sm text-forest">
                  <svg class="w-4 h-4 mr-2 text-leaf" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Nacido: {{ formatDate(baby.birth_date) }}
                </div>
                <div v-if="baby.sex" class="flex items-center text-sm text-forest">
                  <svg class="w-4 h-4 mr-2 text-leaf" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Sexo: {{ baby.sex === 'male' ? 'Masculino' : baby.sex === 'female' ? 'Femenino' : 'Otro' }}
                </div>
                <div v-if="baby.notes" class="text-sm text-forest mt-2">
                  <p class="line-clamp-2">{{ baby.notes }}</p>
                </div>
              </div>

              <!-- Actions -->
              <div class="mt-4 pt-4 border-t border-sage">
                <div class="flex space-x-2">
                  <button
                    @click="viewBabyDetails(baby)"
                    class="flex-1 inline-flex items-center justify-center px-3 py-2 border border-sage text-sm font-medium rounded-md text-forest bg-white hover:bg-mist focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                    Ver Detalles
                  </button>
                  <button
                    @click="editBaby(baby)"
                    class="flex-1 inline-flex items-center justify-center px-3 py-2 border border-sage text-sm font-medium rounded-md text-forest bg-white hover:bg-mist focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf"
                  >
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                    Editar
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add Baby Modal -->
      <div
        v-if="showAddBabyModal"
        class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50"
        @click="showAddBabyModal = false"
      >
        <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white" @click.stop>
          <div class="mt-3">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Agregar Nuevo Bebé</h3>
            <form @submit.prevent="handleAddBaby" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-forest">Nombre</label>
                <input
                  v-model="newBaby.name"
                  type="text"
                  required
                  class="mt-1 block w-full border-sage rounded-md shadow-sm focus:ring-leaf focus:border-leaf"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-forest">Fecha de Nacimiento</label>
                <input
                  v-model="newBaby.birth_date"
                  type="date"
                  required
                  class="mt-1 block w-full border-sage rounded-md shadow-sm focus:ring-leaf focus:border-leaf"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-forest">Sexo</label>
                <select
                  v-model="newBaby.sex"
                  class="mt-1 block w-full border-sage rounded-md shadow-sm focus:ring-leaf focus:border-leaf"
                >
                  <option value="">Seleccionar</option>
                  <option value="male">Masculino</option>
                  <option value="female">Femenino</option>
                  <option value="other">Otro</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-forest">Notas</label>
                <textarea
                  v-model="newBaby.notes"
                  rows="3"
                  class="mt-1 block w-full border-sage rounded-md shadow-sm focus:ring-leaf focus:border-leaf"
                ></textarea>
              </div>
              <div class="flex justify-end space-x-3 pt-4">
                <button
                  type="button"
                  @click="showAddBabyModal = false"
                  class="px-4 py-2 border border-sage rounded-md text-sm font-medium text-forest hover:bg-mist focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="px-4 py-2 border border-transparent rounded-md text-sm font-medium text-white bg-forest hover:bg-leaf focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-leaf disabled:opacity-50"
                >
                  {{ isSubmitting ? 'Agregando...' : 'Agregar Bebé' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useBabiesStore } from '../stores/babies'

const babiesStore = useBabiesStore()

const showAddBabyModal = ref(false)
const isSubmitting = ref(false)
const newBaby = ref({
  name: '',
  birth_date: '',
  sex: '',
  notes: ''
})

// Load babies on component mount
onMounted(() => {
  babiesStore.fetchBabies()
})

// Helper functions
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
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Event handlers
async function handleAddBaby() {
  isSubmitting.value = true
  try {
    await babiesStore.createBaby(newBaby.value)
    showAddBabyModal.value = false
    newBaby.value = { name: '', birth_date: '', sex: '', notes: '' }
  } catch (error) {
    console.error('Error creating baby:', error)
  } finally {
    isSubmitting.value = false
  }
}

function viewBabyDetails(baby) {
  // Navigate to baby detail view (to be implemented)
  console.log('View baby details:', baby)
}

function editBaby(baby) {
  // Navigate to edit baby view (to be implemented)
  console.log('Edit baby:', baby)
}
</script>

<style lang="scss" scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>