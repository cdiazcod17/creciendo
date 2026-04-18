<script setup>
import { useRoute } from "vue-router";
import { useAuthStore } from "./stores/auth";
import AppNavbar from "./components/AppNavbar.vue";
import SiteFooter from "./components/SiteFooter.vue";
import ToastStack from "./components/ToastStack.vue";

const route = useRoute();
const authStore = useAuthStore();

authStore.hydrateFromStorage();
</script>

<template>
  <div class="min-h-screen bg-gray-100 flex flex-col">
    <AppNavbar />
    <main class="flex-1">
      <router-view />
    </main>
    <SiteFooter />
    <ToastStack />
  </div>
</template>

<style scoped></style>