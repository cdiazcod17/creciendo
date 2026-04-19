<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Perfil del bebé</p>
          <h1 class="mt-3 text-3xl font-bold text-ink">{{ baby?.name || 'Detalle del bebé' }}</h1>
          <p class="mt-2 text-sm text-forest/80">Revisa y actualiza la información del bebé. También puedes gestionar sus citas aquí.</p>
        </div>

        <div class="flex flex-wrap gap-2">
          <RouterLink to="/bebes" class="btn-muted">Volver a bebés</RouterLink>
          <button type="button" class="btn-primary bg-red-600 hover:bg-red-700" @click="confirmDeleteBaby">Eliminar bebé</button>
        </div>
      </div>

      <div v-if="babiesStore.isLoading || appointmentsStore.isLoading" class="rounded-3xl bg-white/90 p-8 text-center shadow-sm">
        <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
      </div>

      <div v-else-if="babiesStore.error" class="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700">
        <p class="font-semibold">Error</p>
        <p class="mt-2">{{ babiesStore.error }}</p>
      </div>

      <div v-else-if="!baby" class="rounded-3xl border border-sage bg-white/90 p-8 text-center">
        <p class="text-forest">No se encontró el perfil del bebé.</p>
        <RouterLink to="/bebes" class="btn-primary mt-4 inline-flex">Volver a bebés</RouterLink>
      </div>

      <div v-else class="grid gap-6 lg:grid-cols-[1.05fr_0.95fr]">
        <section class="card space-y-6 rounded-4xl p-6">
          <div class="flex flex-col gap-6 lg:flex-row lg:items-start">
            <div class="flex h-40 w-40 items-center justify-center rounded-4xl bg-mist overflow-hidden">
              <img
                v-if="baby.photo_url"
                :src="baby.photo_url"
                :alt="`Foto de ${baby.name}`"
                class="h-full w-full object-cover"
              />
              <div v-else class="flex h-full w-full items-center justify-center text-forest">
                <svg class="h-14 w-14" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 12c2.21 0 4-1.79 4-4S14.21 4 12 4 8 5.79 8 8s1.79 4 4 4z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 20c0-3.31 2.69-6 6-6s6 2.69 6 6" />
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
                  <p class="mt-2 text-sm text-ink">{{ baby.sex ? baby.sex === 'male' ? 'Masculino' : baby.sex === 'female' ? 'Femenino' : 'Otro' : 'No definido' }}</p>
                </div>
              </div>

              <div class="rounded-3xl border border-sage bg-white p-5">
                <p class="text-sm font-semibold text-forest">Notas</p>
                <p class="mt-3 text-sm leading-6 text-forest/80">{{ baby.notes || 'No hay notas registradas para este bebé.' }}</p>
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
              <textarea v-model="babyForm.notes" rows="4" class="input" placeholder="Observaciones o recordatorios"></textarea>
            </div>

            <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
              <button type="button" class="btn-muted" @click="resetBabyForm">Restablecer</button>
              <button type="submit" class="btn-primary" :disabled="isSavingBaby">{{ isSavingBaby ? 'Guardando...' : 'Guardar cambios' }}</button>
            </div>
          </form>
        </section>
      </div>

      <section class="mt-10 rounded-4xl bg-white/90 p-6 shadow-sm">
        <div class="mb-6 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p class="section-kicker">Citas</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">Gestión de citas</h2>
            <p class="mt-1 text-sm text-forest/75">Revisa, edita y programa citas para este bebé.</p>
          </div>
          <button type="button" class="btn-primary" @click="openAppointmentModal()">Nueva cita</button>
        </div>

        <div v-if="appointmentsStore.error" class="rounded-3xl border border-red-200 bg-red-50 p-5 text-red-700">
          <p class="font-semibold">Error</p>
          <p class="mt-2">{{ appointmentsStore.error }}</p>
        </div>

        <div v-if="!appointmentsStore.appointments.length" class="rounded-3xl border border-sage bg-mist p-8 text-center text-forest/80">
          <p class="text-sm font-semibold">No hay citas registradas.</p>
          <p class="mt-2 text-sm">Agrega la primera cita para este perfil.</p>
        </div>

        <div v-else class="grid gap-4">
          <article
            v-for="appointment in appointmentsStore.appointments"
            :key="appointment.id"
            class="rounded-3xl border border-sage bg-white p-5"
          >
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p class="text-sm font-semibold text-forest">{{ appointment.title }}</p>
                <p class="mt-1 text-sm text-forest/75">{{ formatDateTime(appointment.scheduled_at) }}</p>
              </div>
              <span :class="statusClass(appointment.status)" class="inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]">
                {{ statusLabel(appointment.status) }}
              </span>
            </div>

            <div class="mt-4 grid gap-3 sm:grid-cols-2">
              <div>
                <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Proveedor</p>
                <p class="mt-1 text-sm text-forest/80">{{ appointment.provider_name || 'No definido' }}</p>
              </div>
              <div>
                <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Lugar</p>
                <p class="mt-1 text-sm text-forest/80">{{ appointment.location || 'No definido' }}</p>
              </div>
            </div>

            <p class="mt-4 text-sm leading-6 text-forest/80">{{ appointment.notes || 'Sin notas adicionales' }}</p>

            <div class="mt-5 flex flex-wrap gap-2">
              <button type="button" class="btn-muted" @click="editAppointment(appointment)">Editar</button>
              <button type="button" class="btn-primary bg-red-600 hover:bg-red-700" @click="confirmDeleteAppointment(appointment)">Eliminar</button>
            </div>
          </article>
        </div>
      </section>
    </div>

    <div v-if="showAppointmentForm" class="fixed inset-0 z-50 bg-slate-900/40 px-4 py-6">
      <div class="mx-auto max-w-2xl rounded-3xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="section-kicker">{{ editingAppointment ? 'Editar cita' : 'Nueva cita' }}</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">{{ editingAppointment ? appointmentForm.title : 'Agendar cita' }}</h2>
          </div>
          <button type="button" class="text-forest hover:text-ink" @click="closeAppointmentModal()">✕</button>
        </div>

        <form class="mt-6 space-y-4" @submit.prevent="saveAppointment">
          <div>
            <label class="label">Título</label>
            <input v-model="appointmentForm.title" class="input" required placeholder="Descripción breve" />
          </div>
          <div>
            <label class="label">Fecha y hora</label>
            <input v-model="appointmentForm.scheduled_at" type="datetime-local" class="input" required />
          </div>
          <div>
            <label class="label">Estatus</label>
            <select v-model="appointmentForm.status" class="input">
              <option value="scheduled">Agendada</option>
              <option value="completed">Completada</option>
              <option value="cancelled">Cancelada</option>
            </select>
          </div>
          <div>
            <label class="label">Proveedor</label>
            <input v-model="appointmentForm.provider_name" class="input" placeholder="Nombre del especialista" />
          </div>
          <div>
            <label class="label">Lugar</label>
            <input v-model="appointmentForm.location" class="input" placeholder="Nombre de la clínica o consultorio" />
          </div>
          <div>
            <label class="label">Notas</label>
            <textarea v-model="appointmentForm.notes" rows="4" class="input" placeholder="Observaciones adicionales"></textarea>
          </div>

          <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button type="button" class="btn-muted" @click="closeAppointmentModal()">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="isSavingAppointment">
              {{ isSavingAppointment ? 'Guardando...' : editingAppointment ? 'Actualizar cita' : 'Crear cita' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useBabiesStore } from "../stores/babies";
import { useAppointmentsStore } from "../stores/appointments";
import { useToast } from "../composables/toast";

const route = useRoute();
const router = useRouter();
const toast = useToast();
const babiesStore = useBabiesStore();
const appointmentsStore = useAppointmentsStore();

const showAppointmentForm = ref(false);
const editingAppointment = ref(null);
const isSavingBaby = ref(false);
const isSavingAppointment = ref(false);

const babyForm = reactive({
  name: "",
  birth_date: "",
  sex: "",
  notes: "",
});

const appointmentForm = reactive({
  title: "",
  scheduled_at: "",
  status: "scheduled",
  provider_name: "",
  location: "",
  notes: "",
});

const babyId = computed(() => route.params.babyId);
const baby = computed(() => babiesStore.baby);

function setBabyForm() {
  if (!baby.value) return;
  babyForm.name = baby.value.name || "";
  babyForm.birth_date = baby.value.birth_date || "";
  babyForm.sex = baby.value.sex || "";
  babyForm.notes = baby.value.notes || "";
}

function resetBabyForm() {
  setBabyForm();
}

function formatDate(value) {
  if (!value) return "";
  return new Date(value).toLocaleDateString("es-ES", {
    day: "2-digit",
    month: "long",
    year: "numeric",
  });
}

function formatDateTime(value) {
  if (!value) return "";
  return new Date(value).toLocaleString("es-ES", {
    day: "2-digit",
    month: "long",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

const babyAge = computed(() => {
  if (!baby.value?.birth_date) return "Edad desconocida";
  const birth = new Date(baby.value.birth_date);
  const today = new Date();
  const years = today.getFullYear() - birth.getFullYear();
  const months = today.getMonth() - birth.getMonth() + years * 12;

  if (months < 1) return "Menos de un mes";
  if (months < 12) return `${months} mes${months === 1 ? "" : "es"}`;
  const ageYears = Math.floor(months / 12);
  const remainingMonths = months % 12;
  return `${ageYears} año${ageYears === 1 ? "" : "s"}${remainingMonths ? ` ${remainingMonths} mes${remainingMonths === 1 ? "" : "es"}` : ""}`;
});

function statusLabel(value) {
  return value === "completed" ? "Completada" : value === "cancelled" ? "Cancelada" : "Agendada";
}

function statusClass(value) {
  return value === "completed"
    ? "bg-forest/10 text-forest"
    : value === "cancelled"
    ? "bg-red-100 text-red-700"
    : "bg-leaf/10 text-forest";
}

function openAppointmentModal() {
  editingAppointment.value = null;
  appointmentForm.title = "";
  appointmentForm.scheduled_at = "";
  appointmentForm.status = "scheduled";
  appointmentForm.provider_name = "";
  appointmentForm.location = "";
  appointmentForm.notes = "";
  showAppointmentForm.value = true;
}

function editAppointment(appointment) {
  editingAppointment.value = appointment;
  appointmentForm.title = appointment.title;
  appointmentForm.scheduled_at = appointment.scheduled_at.slice(0, 16);
  appointmentForm.status = appointment.status;
  appointmentForm.provider_name = appointment.provider_name || "";
  appointmentForm.location = appointment.location || "";
  appointmentForm.notes = appointment.notes || "";
  showAppointmentForm.value = true;
}

function closeAppointmentModal() {
  showAppointmentForm.value = false;
  editingAppointment.value = null;
}

async function saveBaby() {
  if (!baby.value) return;
  isSavingBaby.value = true;

  try {
    await babiesStore.updateBaby(baby.value.id, {
      name: babyForm.name,
      birth_date: babyForm.birth_date,
      sex: babyForm.sex || null,
      notes: babyForm.notes || null,
    });
    toast.success("Perfil actualizado", "Los cambios se guardaron correctamente.");
  } catch (error) {
    toast.error("Error", babiesStore.error || "No se pudo guardar el perfil.");
  } finally {
    isSavingBaby.value = false;
  }
}

async function confirmDeleteBaby() {
  if (!baby.value) return;
  const accepted = window.confirm(`¿Eliminar a ${baby.value.name}? Esta acción es irreversible.`);
  if (!accepted) return;

  try {
    await babiesStore.deleteBaby(baby.value.id);
    toast.success("Bebé eliminado", "El perfil fue eliminado correctamente.");
    router.push("/bebes");
  } catch (error) {
    toast.error("Error", babiesStore.error || "No se pudo eliminar el bebé.");
  }
}

async function saveAppointment() {
  if (!baby.value) return;
  isSavingAppointment.value = true;

  try {
    const payload = {
      title: appointmentForm.title,
      scheduled_at: appointmentForm.scheduled_at,
      status: appointmentForm.status,
      provider_name: appointmentForm.provider_name || null,
      location: appointmentForm.location || null,
      notes: appointmentForm.notes || null,
    };

    if (editingAppointment.value) {
      await appointmentsStore.updateAppointment(baby.value.id, editingAppointment.value.id, payload);
      toast.success("Cita actualizada", "Los datos de la cita se guardaron correctamente.");
    } else {
      await appointmentsStore.createAppointment(baby.value.id, payload);
      toast.success("Cita creada", "La cita fue registrada correctamente.");
    }

    closeAppointmentModal();
  } catch (error) {
    toast.error("Error", appointmentsStore.error || "No se pudo guardar la cita.");
  } finally {
    isSavingAppointment.value = false;
  }
}

async function confirmDeleteAppointment(appointment) {
  if (!baby.value) return;
  const accepted = window.confirm(`¿Eliminar la cita “${appointment.title}”?`);
  if (!accepted) return;

  try {
    await appointmentsStore.deleteAppointment(baby.value.id, appointment.id);
    toast.success("Cita eliminada", "La cita fue removida correctamente.");
  } catch (error) {
    toast.error("Error", appointmentsStore.error || "No se pudo eliminar la cita.");
  }
}

watch(babyId, async () => {
  if (!babyId.value) return;
  await babiesStore.fetchBaby(babyId.value);
  setBabyForm();
  await appointmentsStore.fetchAppointments(babyId.value);
});

watch(baby, () => {
  if (baby.value) {
    setBabyForm();
  }
});

if (babyId.value) {
  babiesStore.fetchBaby(babyId.value).then(setBabyForm);
  appointmentsStore.fetchAppointments(babyId.value);
}
</script>
