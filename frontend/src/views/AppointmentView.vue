<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-kicker">Agenda médica</p>
        <h1 class="mt-3 text-4xl font-bold text-ink">Citas del bebé</h1>
        <p class="mt-2 text-sm text-forest/80">
          Gestiona las citas médicas y controles de salud.
        </p>
      </div>

      <!-- Baby Info Card -->
      <div v-if="babiesStore.activeBaby" class="mb-8 rounded-3xl border border-sage bg-white/90 p-6">
        <div class="flex items-center space-x-4">
          <div class="h-16 w-16 overflow-hidden rounded-full bg-leaf/10">
            <img
              v-if="babiesStore.activeBaby.photo_url"
              :src="babiesStore.activeBaby.photo_url"
              :alt="babiesStore.activeBaby.name"
              class="h-full w-full object-cover"
            />
            <div v-else class="flex h-full w-full items-center justify-center">
              <svg class="h-8 w-8 text-leaf/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>
          <div>
            <h2 class="text-xl font-semibold text-ink">{{ babiesStore.activeBaby.name }}</h2>
            <p class="text-sm text-forest/75">
              {{ formatDate(babiesStore.activeBaby.birth_date) }} • {{ getBabyAge(babiesStore.activeBaby.birth_date) }}
            </p>
          </div>
        </div>
      </div>

      <!-- No Active Baby Warning -->
      <div v-else class="mb-8 rounded-3xl border border-red-200 bg-red-50 p-6">
        <div class="flex items-center space-x-3">
          <svg class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <div>
            <h3 class="text-lg font-semibold text-red-800">No hay bebé activo</h3>
            <p class="text-sm text-red-700">Selecciona un bebé activo para gestionar sus citas.</p>
            <RouterLink to="/babies" class="mt-2 inline-flex items-center text-sm font-medium text-red-700 hover:text-red-600">
              Ir a gestión de bebés
              <svg class="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-if="babiesStore.activeBaby" class="grid gap-8 lg:grid-cols-[1fr_400px]">
        <!-- Appointments List -->
        <div class="space-y-6">
          <div class="flex items-center justify-between">
            <h2 class="text-2xl font-semibold text-ink">Citas programadas</h2>
            <button
              @click="showForm = true"
              class="inline-flex items-center rounded-lg bg-leaf px-4 py-2 text-sm font-medium text-white hover:bg-leaf/90"
            >
              <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Nueva cita
            </button>
          </div>

          <!-- Loading State -->
          <div v-if="appointmentsStore.isLoading && !appointmentsStore.appointments.length" class="flex justify-center py-12">
            <div class="h-8 w-8 animate-spin rounded-full border-4 border-leaf border-t-transparent"></div>
          </div>

          <!-- Empty State -->
          <div v-else-if="!appointmentsStore.appointments.length" class="text-center py-12">
            <svg class="mx-auto h-24 w-24 text-forest/30" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            <h3 class="mt-6 text-xl font-semibold text-ink">No hay citas programadas</h3>
            <p class="mt-2 text-sm text-forest/75">Comienza agregando la primera cita médica.</p>
          </div>

          <!-- Appointments List -->
          <div v-else class="space-y-4">
            <div
              v-for="appointment in sortedAppointments"
              :key="appointment.id"
              class="rounded-2xl border border-sage bg-white/90 p-6 transition-all hover:shadow-md"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3">
                    <h3 class="text-lg font-semibold text-ink">{{ appointment.title }}</h3>
                    <span
                      :class="getStatusClasses(appointment.status)"
                      class="rounded-full px-2 py-1 text-xs font-medium"
                    >
                      {{ getStatusText(appointment.status) }}
                    </span>
                  </div>

                  <div class="mt-2 space-y-1 text-sm text-forest/75">
                    <div class="flex items-center">
                      <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      {{ formatDateTime(appointment.scheduled_at) }}
                    </div>

                    <div v-if="appointment.provider_name" class="flex items-center">
                      <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                      {{ appointment.provider_name }}
                    </div>

                    <div v-if="appointment.location" class="flex items-center">
                      <svg class="mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {{ appointment.location }}
                    </div>
                  </div>

                  <p v-if="appointment.notes" class="mt-3 text-sm text-forest/80">
                    {{ appointment.notes }}
                  </p>
                </div>

                <div class="ml-4 flex flex-col space-y-2">
                  <button
                    @click="editAppointment(appointment)"
                    class="rounded-lg p-2 text-forest/60 hover:bg-forest/10 hover:text-forest"
                    title="Editar cita"
                  >
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>

                  <button
                    @click="deleteAppointment(appointment.id)"
                    class="rounded-lg p-2 text-red-400 hover:bg-red-50 hover:text-red-600"
                    title="Eliminar cita"
                  >
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Appointment Form -->
        <div class="space-y-6">
          <div class="rounded-3xl border border-sage bg-white/90 p-6">
            <h3 class="text-xl font-semibold text-ink mb-6">
              {{ editingAppointment ? 'Editar cita' : 'Nueva cita' }}
            </h3>

            <form @submit.prevent="handleSubmit" class="space-y-4">
              <!-- Title -->
              <div>
                <label for="title" class="block text-sm font-medium text-ink">Título *</label>
                <input
                  id="title"
                  v-model="form.title"
                  type="text"
                  required
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                  placeholder="Ej: Control pediátrico, Vacunas, etc."
                />
              </div>

              <!-- Date & Time -->
              <div>
                <label for="scheduled_at" class="block text-sm font-medium text-ink">Fecha y hora *</label>
                <input
                  id="scheduled_at"
                  v-model="form.scheduled_at"
                  type="datetime-local"
                  required
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                />
              </div>

              <!-- Status -->
              <div>
                <label for="status" class="block text-sm font-medium text-ink">Estado</label>
                <select
                  id="status"
                  v-model="form.status"
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                >
                  <option value="scheduled">Programada</option>
                  <option value="confirmed">Confirmada</option>
                  <option value="completed">Completada</option>
                  <option value="cancelled">Cancelada</option>
                </select>
              </div>

              <!-- Provider -->
              <div>
                <label for="provider_name" class="block text-sm font-medium text-ink">Profesional médico</label>
                <input
                  id="provider_name"
                  v-model="form.provider_name"
                  type="text"
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                  placeholder="Nombre del médico o especialista"
                />
              </div>

              <!-- Location -->
              <div>
                <label for="location" class="block text-sm font-medium text-ink">Ubicación</label>
                <input
                  id="location"
                  v-model="form.location"
                  type="text"
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                  placeholder="Clínica, hospital, consultorio"
                />
              </div>

              <!-- Notes -->
              <div>
                <label for="notes" class="block text-sm font-medium text-ink">Notas adicionales</label>
                <textarea
                  id="notes"
                  v-model="form.notes"
                  rows="3"
                  class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
                  placeholder="Detalles adicionales de la cita"
                ></textarea>
              </div>

              <!-- Error Message -->
              <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700">
                <p class="font-semibold">Error</p>
                <p class="mt-1 text-sm">{{ error }}</p>
              </div>

              <!-- Actions -->
              <div class="flex space-x-3 pt-4">
                <button
                  type="button"
                  @click="cancelForm"
                  class="flex-1 rounded-lg border border-sage bg-white py-2 text-sm font-medium text-ink hover:bg-sage/10"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  :disabled="isSubmitting"
                  class="flex-1 rounded-lg bg-leaf py-2 text-sm font-medium text-white hover:bg-leaf/90 disabled:opacity-50"
                >
                  <span v-if="isSubmitting">Guardando...</span>
                  <span v-else>{{ editingAppointment ? 'Actualizar' : 'Crear' }} cita</span>
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
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { useBabiesStore } from '../stores/babies'
import { useAppointmentsStore } from '../stores/appointments'

const babiesStore = useBabiesStore()
const appointmentsStore = useAppointmentsStore()

const showForm = ref(false)
const isSubmitting = ref(false)
const error = ref(null)
const editingAppointment = ref(null)

const form = reactive({
  title: '',
  scheduled_at: '',
  status: 'scheduled',
  provider_name: '',
  location: '',
  notes: ''
})

const sortedAppointments = computed(() => {
  return [...appointmentsStore.appointments].sort((a, b) => {
    return new Date(a.scheduled_at) - new Date(b.scheduled_at)
  })
})

const fetchAppointments = async () => {
  if (babiesStore.activeBabyId) {
    await appointmentsStore.fetchAppointments(babiesStore.activeBabyId)
  }
}

const handleSubmit = async () => {
  if (!babiesStore.activeBabyId) return

  isSubmitting.value = true
  error.value = null

  try {
    const appointmentData = {
      title: form.title,
      scheduled_at: new Date(form.scheduled_at).toISOString(),
      status: form.status,
      provider_name: form.provider_name || null,
      location: form.location || null,
      notes: form.notes || null
    }

    if (editingAppointment.value) {
      await appointmentsStore.updateAppointment(babiesStore.activeBabyId, editingAppointment.value.id, appointmentData)
    } else {
      await appointmentsStore.createAppointment(babiesStore.activeBabyId, appointmentData)
    }

    await fetchAppointments()
    cancelForm()
  } catch (err) {
    error.value = err.message || 'Error al guardar la cita'
  } finally {
    isSubmitting.value = false
  }
}

const editAppointment = (appointment) => {
  editingAppointment.value = appointment
  form.title = appointment.title
  form.scheduled_at = new Date(appointment.scheduled_at).toISOString().slice(0, 16)
  form.status = appointment.status
  form.provider_name = appointment.provider_name || ''
  form.location = appointment.location || ''
  form.notes = appointment.notes || ''
  showForm.value = true
}

const deleteAppointment = async (appointmentId) => {
  if (!babiesStore.activeBabyId) return

  if (confirm('¿Estás seguro de que quieres eliminar esta cita?')) {
    try {
      await appointmentsStore.deleteAppointment(babiesStore.activeBabyId, appointmentId)
      await fetchAppointments()
    } catch (err) {
      error.value = err.message || 'Error al eliminar la cita'
    }
  }
}

const cancelForm = () => {
  editingAppointment.value = null
  form.title = ''
  form.scheduled_at = ''
  form.status = 'scheduled'
  form.provider_name = ''
  form.location = ''
  form.notes = ''
  showForm.value = false
  error.value = null
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getBabyAge = (birthDate) => {
  const today = new Date()
  const birth = new Date(birthDate)
  const ageInMonths = (today.getFullYear() - birth.getFullYear()) * 12 + (today.getMonth() - birth.getMonth())

  if (ageInMonths < 12) {
    return `${ageInMonths} ${ageInMonths === 1 ? 'mes' : 'meses'}`
  } else {
    const years = Math.floor(ageInMonths / 12)
    const months = ageInMonths % 12
    return `${years} ${years === 1 ? 'año' : 'años'}${months > 0 ? ` ${months} ${months === 1 ? 'mes' : 'meses'}` : ''}`
  }
}

const formatDateTime = (dateTimeString) => {
  const date = new Date(dateTimeString)
  return date.toLocaleString('es-ES', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getStatusClasses = (status) => {
  const classes = {
    scheduled: 'bg-blue-100 text-blue-800',
    confirmed: 'bg-green-100 text-green-800',
    completed: 'bg-gray-100 text-gray-800',
    cancelled: 'bg-red-100 text-red-800'
  }
  return classes[status] || classes.scheduled
}

const getStatusText = (status) => {
  const texts = {
    scheduled: 'Programada',
    confirmed: 'Confirmada',
    completed: 'Completada',
    cancelled: 'Cancelada'
  }
  return texts[status] || 'Programada'
}

// Watch for active baby changes
watch(() => babiesStore.activeBabyId, async (newBabyId) => {
  if (newBabyId) {
    await fetchAppointments()
  } else {
    appointmentsStore.appointments = []
  }
})

onMounted(async () => {
  await fetchAppointments()
})
</script>