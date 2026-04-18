<template>
  <div class="pointer-events-none fixed right-4 top-4 z-50 flex w-full max-w-sm flex-col gap-3">
    <TransitionGroup name="toast" tag="div">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="pointer-events-auto rounded-2xl border bg-white/95 px-4 py-3 shadow-lg backdrop-blur"
        :class="toneClass(toast.tone)"
      >
        <p class="text-sm font-semibold">{{ toast.title }}</p>
        <p class="mt-1 text-sm text-black/70">{{ toast.message }}</p>
      </div>
    </TransitionGroup>
  </div>
</template>

<script setup>
import { useToast } from "../composables/toast";

const { toasts } = useToast();

function toneClass(tone) {
  if (tone === "success") {
    return "border-emerald-300";
  }
  if (tone === "error") {
    return "border-red-300";
  }
  return "border-sky-300";
}
</script>
