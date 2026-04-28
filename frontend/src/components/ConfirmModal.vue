<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-[60] flex items-end bg-forest/30 p-3 sm:items-center sm:justify-center sm:p-6">
      <div class="w-full max-w-md rounded-3xl border border-sage bg-white p-5 shadow-xl sm:p-6">
        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-forest/55">Confirmación</p>
        <h3 class="mt-2 font-display text-xl font-semibold text-forest">{{ title }}</h3>
        <p class="mt-2 text-sm leading-6 text-forest/75">{{ message }}</p>

        <div class="mt-5 grid gap-2 sm:grid-cols-2">
          <button class="btn-muted w-full" type="button" :disabled="loading" @click="$emit('cancel')">
            {{ cancelLabel }}
          </button>
          <button class="btn-primary w-full" type="button" :disabled="loading" @click="$emit('confirm')">
            {{ loading ? "Procesando..." : confirmLabel }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: "Confirmar acción",
  },
  message: {
    type: String,
    default: "Esta acción no se puede deshacer.",
  },
  confirmLabel: {
    type: String,
    default: "Confirmar",
  },
  cancelLabel: {
    type: String,
    default: "Cancelar",
  },
  loading: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["cancel", "confirm"]);
</script>