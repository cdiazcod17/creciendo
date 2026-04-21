<template>
  <div class="min-h-screen bg-paper py-10">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p class="section-kicker">Citas</p>
          <h1 class="mt-3 text-3xl font-bold text-ink">Agenda médica</h1>
          <p class="mt-2 text-sm text-forest/80">
            Gestiona las citas del bebé activo o selecciona un perfil en la sección de bebés.
          </p>
        </div>
        <RouterLink v-if="!resolvedBabyId" to="/babies" class="btn-primary">
          Ir a bebés
        </RouterLink>
      </div>

      <div
        v-if="!resolvedBabyId"
        class="rounded-4xl border border-sage bg-white/90 p-8 text-center text-forest/80"
      >
        <p class="text-lg font-semibold">No hay bebé activo</p>
        <p class="mt-3">
          Selecciona un bebé en la pantalla de gestión para empezar a administrar sus citas.
        </p>
        <RouterLink to="/babies" class="btn-primary mt-6 inline-flex">
          Ver bebés
        </RouterLink>
      </div>

      <div v-else>
        <div
          v-if="isBootstrapping || babiesStore.isLoading || appointmentsStore.isLoading"
          class="rounded-3xl bg-white/90 p-8 text-center shadow-sm"
        >
          <div class="inline-flex h-12 w-12 animate-spin rounded-full border-b-2 border-leaf"></div>
        </div>

        <div
          v-else-if="babiesStore.error || appointmentsStore.error"
          class="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700"
        >
          <p class="font-semibold">Error</p>
          <p class="mt-2">{{ babiesStore.error || appointmentsStore.error }}</p>
        </div>

        <div v-else class="grid gap-6 lg:grid-cols-[1fr_0.9fr]">
          <section class="card rounded-4xl p-6">
            <p class="section-kicker">Perfil</p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">{{ baby?.name || "Bebé activo" }}</h2>
            <p class="mt-1 text-sm text-forest/75">
              {{ baby ? `Nacido el ${formatDate(baby.birth_date)}` : "" }}
            </p>

            <div class="mt-6 grid gap-3 sm:grid-cols-2">
              <div class="rounded-3xl border border-sage bg-mist p-4">
                <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Edad</p>
                <p class="mt-2 text-sm text-ink">{{ babyAge }}</p>
              </div>
              <div class="rounded-3xl border border-sage bg-mist p-4">
                <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Sexo</p>
                <p class="mt-2 text-sm text-ink">
                  {{
                    baby?.sex
                      ? baby.sex === "male"
                        ? "Masculino"
                        : baby.sex === "female"
                          ? "Femenino"
                          : "Otro"
                      : "No definido"
                  }}
                </p>
              </div>
            </div>

            <div class="mt-6 rounded-3xl border border-sage bg-white p-4">
              <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Notas</p>
              <p class="mt-2 text-sm text-forest/75">{{ baby?.notes || "Sin notas adicionales" }}</p>
            </div>
          </section>

          <section class="card rounded-4xl p-6">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p class="section-kicker">Acción</p>
                <h2 class="mt-2 text-2xl font-semibold text-ink">Nueva cita</h2>
              </div>
              <button type="button" class="btn-primary" @click="openAppointmentModal()">
                Agregar cita
              </button>
            </div>

            <p class="mt-4 text-sm text-forest/75">
              Las citas estarán vinculadas al perfil seleccionado.
            </p>
          </section>
        </div>

        <section class="mt-8 rounded-4xl border border-sage bg-white/90 p-6">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p class="section-kicker">Lista</p>
              <h2 class="mt-2 text-2xl font-semibold text-ink">Citas del bebé</h2>
            </div>
          </div>

          <div
            v-if="!appointmentsStore.appointments.length"
            class="mt-6 rounded-3xl border border-sage bg-mist p-8 text-center text-forest/80"
          >
            <p class="text-sm font-semibold">No hay citas registradas</p>
            <p class="mt-2">Agrega la primera cita para este bebé desde arriba.</p>
          </div>

          <div v-else class="mt-6 grid gap-4">
            <article
              v-for="appointment in appointmentsStore.appointments"
              :key="appointment.id"
              class="rounded-3xl border border-sage bg-white p-5"
            >
              <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p class="text-sm font-semibold text-forest">{{ appointment.title }}</p>
                  <p class="mt-1 text-sm text-forest/75">
                    {{ formatDateTime(appointment.scheduled_at) }}
                  </p>
                </div>
                <span
                  :class="statusClass(appointment.status)"
                  class="inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em]"
                >
                  {{ statusLabel(appointment.status) }}
                </span>
              </div>

              <div class="mt-4 grid gap-3 sm:grid-cols-2">
                <div>
                  <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Proveedor</p>
                  <p class="mt-1 text-sm text-forest/80">
                    {{ appointment.provider_name || "No definido" }}
                  </p>
                </div>
                <div>
                  <p class="text-xs uppercase tracking-[0.18em] text-forest/50">Lugar</p>
                  <p class="mt-1 text-sm text-forest/80">
                    {{ appointment.location || "No definido" }}
                  </p>
                </div>
              </div>

              <p class="mt-4 text-sm leading-6 text-forest/80">
                {{ appointment.notes || "Sin notas adicionales" }}
              </p>

              <div class="mt-5 flex flex-wrap gap-2">
                <button type="button" class="btn-muted" @click="editAppointment(appointment)">
                  Editar
                </button>
                <button
                  type="button"
                  class="btn-primary bg-red-600 hover:bg-red-700"
                  @click="confirmDeleteAppointment(appointment)"
                >
                  Eliminar
                </button>
              </div>
            </article>
          </div>
        </section>
      </div>
    </div>

    <div v-if="showAppointmentForm" class="fixed inset-0 z-50 bg-slate-900/40 px-4 py-6">
      <div class="mx-auto max-w-2xl rounded-3xl bg-white p-6 shadow-2xl">
        <div class="flex items-start justify-between gap-3">
          <div>
            <p class="section-kicker">
              {{ editingAppointment ? "Editar cita" : "Nueva cita" }}
            </p>
            <h2 class="mt-2 text-2xl font-semibold text-ink">
              {{ editingAppointment ? appointmentForm.title : "Agregar nueva cita" }}
            </h2>
          </div>
          <button type="button" class="text-forest hover:text-ink" @click="closeAppointmentModal()">
            ✕
          </button>
        </div>

        <form class="mt-6 space-y-4" @submit.prevent="saveAppointment">
          <div>
            <label class="label">Título</label>
            <input
              v-model="appointmentForm.title"
              class="input"
              required
              placeholder="Descripción breve"
            />
          </div>

          <div>
            <label class="label">Fecha y hora</label>
            <input
              v-model="appointmentForm.scheduled_at"
              type="datetime-local"
              class="input"
              required
            />
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
            <input
              v-model="appointmentForm.provider_name"
              class="input"
              placeholder="Nombre del especialista"
            />
          </div>

          <div>
            <label class="label">Lugar</label>
            <input
              v-model="appointmentForm.location"
              class="input"
              placeholder="Consultorio, clínica o dirección"
            />
          </div>

          <div>
            <label class="label">Notas</label>
            <textarea
              v-model="appointmentForm.notes"
              rows="4"
              class="input"
              placeholder="Observaciones adicionales"
            ></textarea>
          </div>

          <div class="mt-6 flex flex-col gap-3 sm:flex-row sm:justify-end">
            <button type="button" class="btn-muted" @click="closeAppointmentModal()">
              Cancelar
            </button>
            <button type="submit" class="btn-primary" :disabled="isSavingAppointment">
              {{
                isSavingAppointment
                  ? "Guardando..."
                  : editingAppointment
                    ? "Actualizar cita"
                    : "Crear cita"
              }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, reactive, ref, watch, onMounted } from "vue";
import { useRoute } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { useBabiesStore } from "../stores/babies";
import { useAppointmentsStore } from "../stores/appointments";
import { useToast } from "../composables/toast";

const route = useRoute();
const authStore = useAuthStore();
const babiesStore = useBabiesStore();
const appointmentsStore = useAppointmentsStore();
const toast = useToast();

const showAppointmentForm = ref(false);
const editingAppointment = ref(null);
const isSavingAppointment = ref(false);
const isBootstrapping = ref(false);

const appointmentForm = reactive({
  title: "",
  scheduled_at: "",
  status: "scheduled",
  provider_name: "",
  location: "",
  notes: "",
});

const resolvedBabyId = computed(() => {
  return route.query.babyId || authStore.user?.active_baby_id || babiesStore.activeBabyId || null;
});

const baby = computed(() => babiesStore.baby);

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
  return value === "completed"
    ? "Completada"
    : value === "cancelled"
      ? "Cancelada"
      : "Agendada";
}

function statusClass(value) {
  return value === "completed"
    ? "bg-forest/10 text-forest"
    : value === "cancelled"
      ? "bg-red-100 text-red-700"
      : "bg-leaf/10 text-forest";
}

function resetAppointmentForm() {
  appointmentForm.title = "";
  appointmentForm.scheduled_at = "";
  appointmentForm.status = "scheduled";
  appointmentForm.provider_name = "";
  appointmentForm.location = "";
  appointmentForm.notes = "";
}

function openAppointmentModal() {
  editingAppointment.value = null;
  resetAppointmentForm();
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

async function hydrateContext() {
  isBootstrapping.value = true;

  try {
    await authStore.fetchCurrentUser();

    const babyId = resolvedBabyId.value;
    babiesStore.setActiveBaby(babyId);

    if (!babyId) {
      babiesStore.baby = null;
      return;
    }

    await babiesStore.fetchBaby(babyId);
    await appointmentsStore.fetchAppointments(babyId);
  } finally {
    isBootstrapping.value = false;
  }
}

async function saveAppointment() {
  if (!resolvedBabyId.value) return;

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
      await appointmentsStore.updateAppointment(
        resolvedBabyId.value,
        editingAppointment.value.id,
        payload
      );
      toast.success("Cita actualizada", "Los cambios de la cita se guardaron correctamente.");
    } else {
      await appointmentsStore.createAppointment(resolvedBabyId.value, payload);
      toast.success("Cita creada", "La cita se registró correctamente.");
    }

    closeAppointmentModal();
  } catch (error) {
    toast.error("Error", appointmentsStore.error || "No se pudo guardar la cita.");
  } finally {
    isSavingAppointment.value = false;
  }
}

async function confirmDeleteAppointment(appointment) {
  if (!resolvedBabyId.value) return;

  const accepted = window.confirm(`¿Eliminar la cita “${appointment.title}”?`);
  if (!accepted) return;

  try {
    await appointmentsStore.deleteAppointment(resolvedBabyId.value, appointment.id);
    toast.success("Cita eliminada", "La cita fue eliminada correctamente.");
  } catch (error) {
    toast.error("Error", appointmentsStore.error || "No se pudo eliminar la cita.");
  }
}

watch(
  () => resolvedBabyId.value,
  async (value, previous) => {
    if (!value || value === previous) return;

    babiesStore.setActiveBaby(value);
    await babiesStore.fetchBaby(value);
    await appointmentsStore.fetchAppointments(value);
  }
);

onMounted(async () => {
  await hydrateContext();
});
</script>