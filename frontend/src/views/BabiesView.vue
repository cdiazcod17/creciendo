<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Perfiles</p>
          <h1 class="mt-3 text-3xl font-bold text-ink">Gestión de bebés</h1>
          <p class="mt-2 text-sm text-forest/80">Crea, actualiza y elimina perfiles de bebé con rapidez.</p>
        </div>

        <button class="btn-primary" type="button" @click="openModal()">
          Agregar bebé
        </button>
      </div>

      <div v-if="babiesStore.isLoading" class="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
        <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
      </div>

      <div v-else-if="babiesStore.error" class="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700">
        <p class="font-semibold">Error</p>
        <p class="mt-2">{{ babiesStore.error }}</p>
      </div>

      <div v-else class="space-y-6">
        <div v-if="!babiesStore.babies.length" class="card rounded-3xl border border-sage bg-white/90 text-center">
          <p class="text-sm uppercase tracking-[0.2em] text-forest/50">Sin perfiles</p>
          <h2 class="mt-3 text-xl font-semibold text-ink">No hay bebés registrados todavía</h2>
          <p class="mt-2 text-sm text-forest/75">Agrega el primer bebé y comienza a seguir su crecimiento y citas.</p>
          <button class="btn-primary mt-6" @click="openModal()">Agregar primer bebé</button>
        </div>

        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="item in babiesStore.babies"
            :key="item.id"
            class="card rounded-3xl border border-sage bg-white/90 p-6"
          >
            <div class="flex items-center gap-4">
              <div class="flex h-16 w-16 items-center justify-center rounded-full bg-mist text-forest">
                <svg class="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
                </svg>
              </div>
              <div>
                <p class="text-sm uppercase tracking-[0.18em] text-forest/60">{{ item.sex ? item.sex.charAt(0).toUpperCase() + item.sex.slice(1) : 'Sin sexo' }}</p>
                <h2 class="text-xl font-semibold text-ink">{{ item.name }}</h2>
                <p class="text-sm text-forest/75">{{ formatDate(item.birth_date) }}</p>
              </div>
            </div>

            <p class="mt-4 text-sm leading-6 text-forest/80 line-clamp-3">{{ item.notes || 'Sin notas adicionales' }}</p>

            <div class="mt-6 flex flex-wrap gap-2">
              <RouterLink :to="`/bebes/${item.id}`" class="btn-muted">Ver</RouterLink>
              <button type="button" class="btn-muted" @click="openModal(item)">Editar</button>
              <button type="button" class="btn-primary bg-red-600 hover:bg-red-700" @click="confirmDelete(item)">Eliminar</button>
            </div>
          </article>
        </div>
      </div>
    </div>

    <div v-if="showForm" class="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 px-4 py-6">
      <div class="mx-auto w-full max-w-xl rounded-3xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="section-kicker">{{ editMode ? 'Editar bebé' : 'Nuevo bebé' }}</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">{{ editMode ? babyForm.name : 'Agrega un perfil' }}</h2>
          </div>
          <button type="button" class="text-forest hover:text-ink" @click="closeModal()">✕</button>
        </div>

        <form class="mt-6 space-y-4" @submit.prevent="saveBaby">
          <div>
            <label class="label">Nombre</label>
            <input v-model="babyForm.name" class="input" required placeholder="Nombre del bebé" />
          </div>
          <div>
            <label class="label">Fecha de nacimiento</label>
            <input v-model="babyForm.birth_date" type="date" class="input" required />
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
            <label class="label">Notas</label>
            <textarea v-model="babyForm.notes" rows="4" class="input" placeholder="Observaciones o datos importantes"></textarea>
          </div>

          <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button type="button" class="btn-muted" @click="closeModal()">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? 'Guardando...' : editMode ? 'Actualizar bebé' : 'Crear bebé' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useBabiesStore } from "../stores/babies";
import { useToast } from "../composables/toast";

const babiesStore = useBabiesStore();
const toast = useToast();

const showForm = ref(false);
const editMode = ref(false);
const isSubmitting = ref(false);
const currentBaby = ref(null);

const babyForm = reactive({
  name: "",
  birth_date: "",
  sex: "",
  notes: "",
});

function resetForm() {
  currentBaby.value = null;
  editMode.value = false;
  babyForm.name = "";
  babyForm.birth_date = "";
  babyForm.sex = "";
  babyForm.notes = "";
}

function openModal(baby = null) {
  resetForm();

  if (baby) {
    editMode.value = true;
    currentBaby.value = baby;
    babyForm.name = baby.name || "";
    babyForm.birth_date = baby.birth_date || "";
    babyForm.sex = baby.sex || "";
    babyForm.notes = baby.notes || "";
  }

  showForm.value = true;
}

function closeModal() {
  showForm.value = false;
  resetForm();
}

async function saveBaby() {
  isSubmitting.value = true;

  try {
    if (editMode.value && currentBaby.value) {
      await babiesStore.updateBaby(currentBaby.value.id, {
        name: babyForm.name,
        birth_date: babyForm.birth_date,
        sex: babyForm.sex || null,
        notes: babyForm.notes || null,
      });
      toast.success("Perfil actualizado", "Los datos del bebé se guardaron correctamente.");
    } else {
      await babiesStore.createBaby({
        name: babyForm.name,
        birth_date: babyForm.birth_date,
        sex: babyForm.sex || null,
        notes: babyForm.notes || null,
      });
      toast.success("Bebé registrado", "El perfil del bebé fue creado correctamente.");
    }
    closeModal();
  } catch (error) {
    toast.error("Error", babiesStore.error || "Hubo un problema al guardar el bebé.");
  } finally {
    isSubmitting.value = false;
  }
}

async function confirmDelete(baby) {
  const confirmed = window.confirm(`¿Eliminar a ${baby.name}? Esta acción no se puede deshacer.`);
  if (!confirmed) return;

  try {
    await babiesStore.deleteBaby(baby.id);
    toast.success("Bebé eliminado", "El perfil fue borrado correctamente.");
  } catch (error) {
    toast.error("Error", babiesStore.error || "No se pudo eliminar el bebé.");
  }
}

function formatDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}

babiesStore.fetchBabies();
</script>
