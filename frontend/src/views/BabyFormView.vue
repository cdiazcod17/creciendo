<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-2xl px-4 sm:px-6 lg:px-8">
      <div class="mb-10">
        <p class="section-kicker">{{ isEditing ? 'Editar' : 'Nuevo' }} perfil</p>
        <h1 class="mt-3 text-4xl font-bold text-ink">
          {{ isEditing ? 'Editar bebé' : 'Agregar bebé' }}
        </h1>
        <p class="mt-2 text-sm text-forest/80">
          {{ isEditing ? 'Actualiza la información del perfil.' : 'Completa los datos para crear un nuevo perfil de bebé.' }}
        </p>
      </div>

      <form @submit.prevent="handleSubmit" class="card space-y-6 rounded-3xl p-8">
        <!-- Foto -->
        <div class="flex flex-col items-center space-y-4">
          <div class="relative">
            <div class="h-32 w-32 overflow-hidden rounded-full bg-leaf/10">
              <img
                v-if="form.photo_url"
                :src="form.photo_url"
                alt="Foto del bebé"
                class="h-full w-full object-cover"
              />
              <div v-else class="flex h-full w-full items-center justify-center">
                <svg class="h-12 w-12 text-leaf/50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
              </div>
            </div>
            <button
              type="button"
              @click="triggerFileInput"
              class="absolute bottom-0 right-0 rounded-full bg-leaf p-2 text-white shadow-lg hover:bg-leaf/90"
            >
              <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
          </div>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileChange"
            class="hidden"
          />
          <p class="text-xs text-forest/60">Haz clic para cambiar la foto</p>
        </div>

        <!-- Nombre -->
        <div>
          <label for="name" class="block text-sm font-medium text-ink">Nombre *</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            required
            class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Ingresa el nombre del bebé"
          />
        </div>

        <!-- Fecha de naciomiento -->
        <div>
          <label for="birth_date" class="block text-sm font-medium text-ink">Fecha de nacimiento *</label>
          <input
            id="birth_date"
            v-model="form.birth_date"
            type="date"
            required
            class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
          />
        </div>

        <!-- Genero -->
        <div>
          <label class="block text-sm font-medium text-ink">Sexo</label>
          <div class="mt-2 space-y-2">
            <label class="flex items-center">
              <input
                v-model="form.sex"
                type="radio"
                value="M"
                class="h-4 w-4 text-leaf focus:ring-leaf"
              />
              <span class="ml-2 text-sm text-ink">Masculino</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.sex"
                type="radio"
                value="F"
                class="h-4 w-4 text-leaf focus:ring-leaf"
              />
              <span class="ml-2 text-sm text-ink">Femenino</span>
            </label>
            <label class="flex items-center">
              <input
                v-model="form.sex"
                type="radio"
                value=""
                class="h-4 w-4 text-leaf focus:ring-leaf"
              />
              <span class="ml-2 text-sm text-ink">Prefiero no especificar</span>
            </label>
          </div>
        </div>

        <!-- Notas -->
        <div>
          <label for="notes" class="block text-sm font-medium text-ink">Notas adicionales</label>
          <textarea
            id="notes"
            v-model="form.notes"
            rows="3"
            class="mt-1 block w-full rounded-lg border border-sage bg-white px-3 py-2 text-ink placeholder-forest/50 focus:border-leaf focus:outline-none focus:ring-1 focus:ring-leaf"
            placeholder="Información adicional sobre el bebé (opcional)"
          ></textarea>
        </div>

        <!-- Error Message -->
        <div v-if="error" class="rounded-lg bg-red-50 p-4 text-red-700">
          <p class="font-semibold">Error</p>
          <p class="mt-1 text-sm">{{ error }}</p>
        </div>

        <!-- Acciones -->
        <div class="flex flex-col gap-3 sm:flex-row sm:justify-end">
          <RouterLink
            to="/babies"
            class="btn-muted order-2 sm:order-1"
          >
            Cancelar
          </RouterLink>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="btn-primary order-1 sm:order-2 disabled:opacity-50"
          >
            <span v-if="isSubmitting" class="inline-flex items-center">
              <svg class="mr-2 h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Guardando...
            </span>
            <span v-else>{{ isEditing ? 'Actualizar' : 'Crear' }} bebé</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBabiesStore } from '../stores/babies'

const route = useRoute()
const router = useRouter()
const babiesStore = useBabiesStore()

const fileInput = ref(null)
const isSubmitting = ref(false)
const error = ref(null)

const isEditing = computed(() => route.params.babyId && route.params.babyId !== 'new')

const form = reactive({
  name: '',
  birth_date: '',
  sex: '',
  notes: '',
  photo_url: null
})

const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    // Aquí normalmente subirías la imagen a un servicio de almacenamiento
    // Por ahora, solo guardamos la URL temporal
    const reader = new FileReader()
    reader.onload = (e) => {
      form.photo_url = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const handleSubmit = async () => {
  isSubmitting.value = true
  error.value = null

  try {
    const babyData = {
      name: form.name,
      birth_date: form.birth_date,
      sex: form.sex || null,
      notes: form.notes || null,
      photo_url: form.photo_url
    }

    if (isEditing.value) {
      await babiesStore.updateBaby(route.params.babyId, babyData)
    } else {
      await babiesStore.createBaby(babyData)
    }

    router.push('/babies')
  } catch (err) {
    error.value = err.message || 'Error al guardar el bebé'
  } finally {
    isSubmitting.value = false
  }
}

onMounted(async () => {
  if (isEditing.value) {
    try {
      const baby = await babiesStore.fetchBaby(route.params.babyId)
      if (baby) {
        form.name = baby.name
        form.birth_date = baby.birth_date.split('T')[0] // Convertir formato ISO a YYYY-MM-DD
        form.sex = baby.sex || ''
        form.notes = baby.notes || ''
        form.photo_url = baby.photo_url
      }
    } catch (err) {
      error.value = 'Error al cargar los datos del bebé'
    }
  }
})
</script>