<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Perfil del bebé</p>
          <h1 class="mt-3 text-3xl font-bold text-ink">
            {{ baby?.name || 'Detalle del bebé' }}
          </h1>
          <p class="mt-2 text-sm text-forest/80">
            Revisa y actualiza la información general del bebé.
          </p>
        </div>

        <div class="flex flex-wrap gap-2">
          <RouterLink to="/dashboard" class="btn-muted">Volver al Dashboard</RouterLink>
          <button
            type="button"
            class="btn-primary bg-red-600 hover:bg-red-700"
            @click="confirmDeleteBaby"
          >
            Eliminar bebé
          </button>
        </div>
      </div>

      <div v-if="babiesStore.isLoading" class="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
        <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
      </div>

      <div v-else-if="babiesStore.error" class="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700">
        <p class="font-semibold">Error</p>
        <p class="mt-2">{{ babiesStore.error }}</p>
      </div>

      <div v-else-if="!baby" class="rounded-3xl border border-sage bg-white/90 p-8 text-center">
        <p class="text-forest">No se encontró el perfil del bebé.</p>
        <RouterLink to="/babies" class="btn-primary mt-4 inline-flex">
          Volver a bebés
        </RouterLink>
      </div>

      <div v-else class="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <section class="card space-y-6 rounded-4xl p-6">
          <div class="flex flex-col gap-6 lg:flex-row lg:items-start">
            <div class="flex h-40 w-40 items-center justify-center overflow-hidden rounded-4xl bg-mist">
              <img
                v-if="baby.photo_url"
                :src="baby.photo_url"
                :alt="`Foto de ${baby.name}`"
                class="h-full w-full object-cover"
              />
              <div v-else class="flex h-full w-full items-center justify-center text-forest">
                <svg class="h-14 w-14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z"
                  />
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6"
                  />
                </svg>
              </div>
            </div>

            <div class="space-y-5">
              <div>
                <p class="text-sm uppercase tracking-[0.2em] text-forest/50">Datos del bebé</p>
                <h2 class="mt-2 text-3xl font-semibold text-ink">{{ baby.name }}</h2>
                <p class="mt-1 text-sm text-forest/75">{{ babyAge }}</p>
              </div>

              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-3xl border border-sage bg-mist p-4">
                  <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Fecha de nacimiento</p>
                  <p class="mt-2 text-sm text-ink">{{ formatDate(baby.birth_date) }}</p>
                </div>

                <div class="rounded-3xl border border-sage bg-mist p-4">
                  <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Sexo</p>
                  <p class="mt-2 text-sm text-ink">
                    {{
                      baby.sex
                        ? baby.sex === 'male'
                          ? 'Masculino'
                          : baby.sex === 'female'
                            ? 'Femenino'
                            : 'Otro'
                        : 'No definido'
                    }}
                  </p>
                </div>
              </div>

              <div class="rounded-3xl border border-sage bg-white p-5">
                <p class="text-sm font-semibold text-forest">Notas</p>
                <p class="mt-3 text-sm leading-6 text-forest/80">
                  {{ baby.notes || 'No hay notas registradas para este bebé.' }}
                </p>
              </div>
            </div>
          </div>
        </section>

        <section class="card rounded-4xl p-6">
          <p class="section-kicker">Editar perfil</p>
          <h2 class="mt-2 text-2xl font-semibold text-ink">Actualizar información</h2>

          <form class="mt-6 space-y-4" @submit.prevent="saveBaby">
            <div>
              <label class="label">Nombre</label>
              <input
                v-model="babyForm.name"
                class="input"
                required
                placeholder="Nombre del bebé"
              />
            </div>

            <div>
              <label class="label">Fecha de nacimiento</label>
              <input
                v-model="babyForm.birth_date"
                type="date"
                class="input"
                required
              />
            </div>

            <div>
              <label class="label">Sexo</label>
              <select v-model="babyForm.sex" class="input">
                <option value="">Seleccionar</option>
                <option value="male">Masculino</option>
                <option value="female">Femenino</option>
                <option value="other">Otro</option>
              </select>
            </div>

            <div>
              <label class="label">Foto (URL)</label>
              <input
                v-model="babyForm.photo_url"
                type="url"
                class="input"
                placeholder="https://ejemplo.com/foto.jpg"
              />
            </div>

            <div>
              <label class="label">Notas</label>
              <textarea
                v-model="babyForm.notes"
                rows="4"
                class="input"
                placeholder="Observaciones o recordatorios"
              ></textarea>
            </div>

            <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button type="button" class="btn-muted" @click="resetBabyForm">
                Restablecer
              </button>
              <button type="submit" class="btn-primary" :disabled="isSavingBaby">
                {{ isSavingBaby ? 'Guardando...' : 'Guardar cambios' }}
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useBabiesStore } from '../stores/babies'
import { useToast } from '../composables/toast'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const babiesStore = useBabiesStore()

const isSavingBaby = ref(false)

const babyForm = reactive({
  name: '',
  birth_date: '',
  sex: '',
  notes: '',
  photo_url: '',
})

const babyId = computed(() => route.params.babyId)
const baby = computed(() => babiesStore.baby)

function setBabyForm() {
  if (!baby.value) return

  babyForm.name = baby.value.name || ''
  babyForm.birth_date = baby.value.birth_date || ''
  babyForm.sex = baby.value.sex || ''
  babyForm.notes = baby.value.notes || ''
  babyForm.photo_url = baby.value.photo_url || ''
}

function resetBabyForm() {
  setBabyForm()
}

function formatDate(value) {
  if (!value) return ''

  return new Date(value).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'long',
    year: 'numeric',
  })
}

const babyAge = computed(() => {
  if (!baby.value?.birth_date) return 'Edad desconocida'

  const birth = new Date(baby.value.birth_date)
  const today = new Date()
  const years = today.getFullYear() - birth.getFullYear()
  const months = today.getMonth() - birth.getMonth() + years * 12

  if (months < 1) return 'Menos de un mes'
  if (months < 12) return `${months} mes${months === 1 ? '' : 'es'}`

  const ageYears = Math.floor(months / 12)
  const remainingMonths = months % 12

  return `${ageYears} año${ageYears === 1 ? '' : 's'}${remainingMonths ? ` ${remainingMonths} mes${remainingMonths === 1 ? '' : 'es'}` : ''}`
})

async function saveBaby() {
  if (!baby.value) return

  isSavingBaby.value = true

  try {
    await babiesStore.updateBaby(baby.value.id, {
      name: babyForm.name,
      birth_date: babyForm.birth_date,
      sex: babyForm.sex || null,
      notes: babyForm.notes || null,
      photo_url: babyForm.photo_url || null,
    })

    toast.success('Perfil actualizado', 'Los cambios se guardaron correctamente.')
  } catch (error) {
    toast.error('Error', babiesStore.error || 'No se pudo guardar el perfil.')
  } finally {
    isSavingBaby.value = false
  }
}

async function confirmDeleteBaby() {
  if (!baby.value) return

  const accepted = window.confirm(`¿Eliminar a ${baby.value.name}? Esta acción es irreversible.`)
  if (!accepted) return

  try {
    await babiesStore.deleteBaby(baby.value.id)
    toast.success('Bebé eliminado', 'El perfil fue eliminado correctamente.')
    router.push('/babies')
  } catch (error) {
    toast.error('Error', babiesStore.error || 'No se pudo eliminar el bebé.')
  }
}

watch(babyId, async () => {
  if (!babyId.value) return
  await babiesStore.fetchBaby(babyId.value)
  setBabyForm()
})

watch(baby, () => {
  if (baby.value) {
    setBabyForm()
  }
})

if (babyId.value) {
  babiesStore.fetchBaby(babyId.value).then(setBabyForm)
}
</script>