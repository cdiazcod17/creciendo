<template>
  <RouterLink to="/" class="inline-flex items-center gap-2.5 sm:gap-3">
    <div class="flex h-10 w-10 items-center justify-center overflow-hidden rounded-2xl bg-white ring-1 ring-sage shadow-sm sm:h-12 sm:w-12">
      <img class="h-8 w-8 object-contain sm:h-10 sm:w-10" src="../../public/creciendo-logo.svg" alt="Logo de Creciendo" />
    </div>
    <div v-if="showLabel">
      <p class="font-display text-base font-semibold text-forest sm:text-lg">Creciendo</p>
    </div>
  </RouterLink>
</template>

<script setup>
defineProps({
  showLabel: {
    type: Boolean,
    default: true,
  },
});
</script>
