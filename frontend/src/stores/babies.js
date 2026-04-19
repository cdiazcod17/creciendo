import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { babiesApi } from '../services/babies'

function normalizeError(error, fallback) {
  return error?.response?.data?.detail || error?.message || fallback
}

export const useBabiesStore = defineStore('babies', () => {
  const babies = ref([])
  const baby = ref(null)
  const activeBabyId = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  const activeBaby = computed(() => {
    return babies.value.find((item) => item.id === activeBabyId.value) || null
  })

  const hasBabies = computed(() => babies.value.length > 0)

  function ensureActiveBaby() {
    if (!babies.value.length) {
      activeBabyId.value = null
      return
    }

    const exists = babies.value.some((item) => item.id === activeBabyId.value)

    if (!activeBabyId.value || !exists) {
      activeBabyId.value = babies.value[0].id
    }
  }

  async function fetchBabies() {
    isLoading.value = true
    error.value = null

    try {
      const data = await babiesApi.listBabies()
      babies.value = data
      ensureActiveBaby()
      return data
    } catch (err) {
      error.value = normalizeError(err, 'Error al cargar bebés')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchBaby(babyId) {
    if (!babyId) {
      baby.value = null
      return null
    }

    isLoading.value = true
    error.value = null

    try {
      const data = await babiesApi.getBaby(babyId)
      baby.value = data
      return data
    } catch (err) {
      error.value = normalizeError(err, 'Error al cargar bebé')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function createBaby(babyData) {
    isLoading.value = true
    error.value = null

    try {
      const newBaby = await babiesApi.createBaby(babyData)
      babies.value.push(newBaby)

      if (babies.value.length === 1) {
        activeBabyId.value = newBaby.id
      }

      return newBaby
    } catch (err) {
      error.value = normalizeError(err, 'Error al crear bebé')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function setActiveBaby(babyId) {
    activeBabyId.value = babyId
  }

  async function updateBaby(babyId, babyData) {
    isLoading.value = true
    error.value = null

    try {
      const updatedBaby = await babiesApi.updateBaby(babyId, babyData)

      babies.value = babies.value.map((item) =>
        item.id === babyId ? updatedBaby : item
      )

      if (baby.value?.id === babyId) {
        baby.value = updatedBaby
      }

      return updatedBaby
    } catch (err) {
      error.value = normalizeError(err, 'Error al actualizar bebé')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function deleteBaby(babyId) {
    isLoading.value = true
    error.value = null

    try {
      await babiesApi.deleteBaby(babyId)

      babies.value = babies.value.filter((item) => item.id !== babyId)

      if (baby.value?.id === babyId) {
        baby.value = null
      }

      ensureActiveBaby()
    } catch (err) {
      error.value = normalizeError(err, 'Error al eliminar bebé')
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    babies,
    baby,
    activeBabyId,
    activeBaby,
    isLoading,
    error,
    hasBabies,
    fetchBabies,
    fetchBaby,
    createBaby,
    setActiveBaby,
    updateBaby,
    deleteBaby,
  }
})