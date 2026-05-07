<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="mb-10 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Evolución</p>
          <h1 class="mt-3 text-4xl font-bold text-ink">Crecimiento</h1>
          <p class="mt-2 text-sm text-forest/80">
            Seguimiento de peso, talla y perímetro cefálico.
          </p>
        </div>
        <div class="flex flex-wrap gap-2">
          <RouterLink to="/dashboard" class="btn-muted">
            Volver al Dashboard
          </RouterLink>
        </div>
      </div>

      <!-- Baby Info Card (Shared pattern) -->
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
              {{ formatDateDisplay(babiesStore.activeBaby.birth_date) }} • {{ getBabyAge(babiesStore.activeBaby.birth_date) }}
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
            <p class="text-sm text-red-700">Selecciona un bebé para ver su historial de crecimiento.</p>
            <RouterLink to="/babies" class="mt-2 inline-flex items-center text-sm font-medium text-red-700 hover:text-red-600">
              Ir a gestión de bebés
              <svg class="ml-1 h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </RouterLink>
          </div>
        </div>
      </div>

      <div v-if="babiesStore.activeBaby" class="grid gap-8 lg:grid-cols-[1fr_2fr]">
        <!-- Action Panel -->
        <section class="space-y-6">
          <div class="card rounded-4xl p-6">
            <p class="section-kicker">Nuevo registro</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">Registrar medidas</h2>
            <p class="mt-1 text-sm text-forest/70">Ingresa los datos del control actual.</p>
            
            <button 
              @click="openNewForm"
              class="btn-primary w-full mt-6"
            >
              Agregar medidas
            </button>
          </div>
          
          <!-- Summary card (Optional: Last measures) -->
          <div v-if="growthStore.sortedRecords.length > 0" class="card rounded-4xl p-6 bg-mist/30">
            <p class="section-kicker">Último control</p>
            <div class="mt-4 grid grid-cols-2 gap-4">
              <div v-if="growthStore.sortedRecords[0].weight_kg">
                <p class="text-[10px] uppercase tracking-widest text-forest/50">Peso</p>
                <p class="text-lg font-bold text-forest">{{ growthStore.sortedRecords[0].weight_kg }} kg</p>
              </div>
              <div v-if="growthStore.sortedRecords[0].height_cm">
                <p class="text-[10px] uppercase tracking-widest text-forest/50">Talla</p>
                <p class="text-lg font-bold text-forest">{{ growthStore.sortedRecords[0].height_cm }} cm</p>
              </div>
            </div>
            <p class="mt-4 text-[11px] text-forest/40">
              Registrado el {{ formatDateDisplay(growthStore.sortedRecords[0].measured_at) }}
            </p>
          </div>
        </section>

        <!-- History List -->
        <section class="card rounded-4xl p-6">
          <div class="flex items-center justify-between mb-8">
            <h2 class="text-2xl font-semibold text-ink">Historial</h2>
          </div>

          <!-- Loading -->
          <div v-if="growthStore.isLoading && !growthStore.records.length" class="flex justify-center py-12">
            <div class="h-10 w-10 animate-spin rounded-full border-b-2 border-leaf"></div>
          </div>

          <!-- Empty -->
          <div v-else-if="!growthStore.records.length" class="py-12 text-center">
            <div class="h-16 w-16 bg-mist rounded-full flex items-center justify-center mx-auto text-forest/30 mb-4">
              <svg class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
              </svg>
            </div>
            <p class="text-forest/75 font-medium">Sin registros aún</p>
            <p class="text-sm text-forest/50 mt-1">Registra las medidas de crecimiento para ver la evolución.</p>
          </div>

          <!-- List -->
          <div v-else class="space-y-4">
            <article 
              v-for="record in growthStore.sortedRecords" 
              :key="record.id"
              class="group relative flex items-center gap-4 p-5 rounded-3xl border border-sage bg-white hover:shadow-md transition-all"
            >
              <div class="h-12 w-12 rounded-2xl bg-leaf/10 flex items-center justify-center text-leaf">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>

              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between">
                  <time class="font-bold text-ink text-sm">{{ formatDateDisplay(record.measured_at) }}</time>
                  <div class="flex gap-4">
                    <span v-if="record.weight_kg" class="text-xs font-semibold text-forest/70">{{ record.weight_kg }} kg</span>
                    <span v-if="record.height_cm" class="text-xs font-semibold text-forest/70">{{ record.height_cm }} cm</span>
                  </div>
                </div>
                <p v-if="record.head_circumference_cm" class="mt-1 text-xs text-forest/50">
                  PC: {{ record.head_circumference_cm }} cm
                </p>
                <p v-if="record.notes" class="mt-2 text-xs text-forest/60 italic line-clamp-1">
                  "{{ record.notes }}"
                </p>
              </div>

              <!-- Actions -->
              <div class="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                <button @click="editRecord(record)" class="p-2 text-forest/60 hover:text-leaf hover:bg-leaf/10 rounded-lg">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                </button>
                <button @click="confirmDeleteRecord(record)" class="p-2 text-forest/60 hover:text-red-600 hover:bg-red-50 rounded-lg">
                  <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="fixed inset-0 z-50 bg-slate-900/40 px-4 py-6 flex items-center justify-center overflow-y-auto">
      <div class="w-full max-w-lg rounded-3xl bg-white p-6 shadow-2xl my-auto animate-in fade-in zoom-in duration-200">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-ink">
            {{ editingRecord ? 'Editar registro' : 'Nuevo registro' }}
          </h2>
          <button @click="closeForm" class="text-forest/40 hover:text-ink">
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <form @submit.prevent="saveRecord" class="space-y-4">
          <div>
            <label class="label">Fecha del control</label>
            <input v-model="form.measured_at" type="datetime-local" class="input" required />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Peso (kg)</label>
              <input v-model.number="form.weight_kg" type="number" step="0.01" min="0" class="input" placeholder="Ej: 3.50" />
            </div>
            <div>
              <label class="label">Talla (cm)</label>
              <input v-model.number="form.height_cm" type="number" step="0.1" min="0" class="input" placeholder="Ej: 52.0" />
            </div>
          </div>

          <div>
            <label class="label">Perímetro cefálico (cm)</label>
            <input v-model.number="form.head_circumference_cm" type="number" step="0.1" min="0" class="input" placeholder="Opcional" />
          </div>

          <div>
            <label class="label">Notas / Observaciones</label>
            <textarea v-model="form.notes" rows="3" class="input" placeholder="Ej: Control de primer mes"></textarea>
          </div>

          <div v-if="localError" class="text-xs text-red-500 font-semibold">{{ localError }}</div>

          <div class="pt-4 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button type="button" class="btn-muted" @click="closeForm">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : (editingRecord ? 'Actualizar' : 'Registrar') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from "vue";
import { useBabiesStore } from "../stores/babies";
import { useGrowthStore } from "../stores/growth";
import { useToast } from "../composables/toast";

const babiesStore = useBabiesStore();
const growthStore = useGrowthStore();
const toast = useToast();

const showForm = ref(false);
const isSaving = ref(false);
const editingRecord = ref(null);
const localError = ref("");

const form = reactive({
  measured_at: "",
  weight_kg: null,
  height_cm: null,
  head_circumference_cm: null,
  notes: "",
});

const formatDateDisplay = (val) => {
  if (!val) return "";
  return new Date(val).toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
};

const getBabyAge = (birthDate) => {
  if (!birthDate) return "";
  const today = new Date();
  const birth = new Date(birthDate);
  const diffTime = Math.abs(today - birth);
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  if (diffDays < 30) return `${diffDays} días`;
  const diffMonths = Math.floor(diffDays / 30.44);
  if (diffMonths < 12) return `${diffMonths} meses`;
  const diffYears = Math.floor(diffMonths / 12);
  const remMonths = diffMonths % 12;
  return `${diffYears} año${diffYears > 1 ? "s" : ""}${remMonths ? ` y ${remMonths} m` : ""}`;
};

async function loadData() {
  if (babiesStore.activeBabyId) {
    await growthStore.fetchRecords(babiesStore.activeBabyId);
  }
}

function openNewForm() {
  editingRecord.value = null;
  // Use local time for initial value
  const now = new Date();
  form.measured_at = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  form.weight_kg = null;
  form.height_cm = null;
  form.head_circumference_cm = null;
  form.notes = "";
  localError.value = "";
  showForm.value = true;
}

function editRecord(record) {
  editingRecord.value = record;
  // Convert UTC from API to local time for input
  const date = new Date(record.measured_at);
  form.measured_at = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
  form.weight_kg = record.weight_kg;
  form.height_cm = record.height_cm;
  form.head_circumference_cm = record.head_circumference_cm;
  form.notes = record.notes || "";
  localError.value = "";
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editingRecord.value = null;
}

async function saveRecord() {
  if (!babiesStore.activeBabyId) return;
  
  // Validation: at least one measure
  if (!form.weight_kg && !form.height_cm && !form.head_circumference_cm) {
    localError.value = "Debes ingresar al menos una medida (peso, talla o PC).";
    return;
  }

  isSaving.value = true;
  localError.value = "";
  try {
    const payload = { 
      ...form,
      measured_at: new Date(form.measured_at).toISOString() 
    };
    
    // Clean nulls to avoid API validation errors if needed, though Pydantic handles it
    if (editingRecord.value) {
      await growthStore.updateRecord(babiesStore.activeBabyId, editingRecord.value.id, payload);
      toast.success("Registro actualizado", "Las medidas han sido guardadas.");
    } else {
      await growthStore.createRecord(babiesStore.activeBabyId, payload);
      toast.success("Registro creado", "Nuevas medidas registradas correctamente.");
    }
    closeForm();
  } catch (err) {
    localError.value = growthStore.error || "Ocurrió un error al guardar.";
  } finally {
    isSaving.value = false;
  }
}

async function confirmDeleteRecord(record) {
  if (window.confirm("¿Estás seguro de que quieres eliminar este registro de crecimiento?")) {
    try {
      await growthStore.deleteRecord(babiesStore.activeBabyId, record.id);
      toast.success("Eliminado", "Registro borrado exitosamente.");
    } catch (err) {
      toast.error("Error", "No se pudo eliminar el registro.");
    }
  }
}

watch(() => babiesStore.activeBabyId, loadData);
onMounted(loadData);
</script>
