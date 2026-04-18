<template>
  <header class="sticky top-0 z-40 border-b border-forest/10 bg-paper/85 backdrop-blur">
    <div class="mx-auto max-w-6xl px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between gap-3">
        <AppLogo />

        <nav class="hidden items-center gap-6 md:flex">
          <template v-if="authStore.isAuthenticated">
            <RouterLink class="nav-link" :to="primaryAuthenticatedRoute">{{ primaryAuthenticatedLabel }}</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/eventos">Eventos</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/citas">Citas</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/crecimiento">Crecimiento</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/salud">Salud</RouterLink>
            <RouterLink class="nav-link" to="/bebes">Bebes</RouterLink>
          </template>
          <template v-else>
            <RouterLink class="nav-link" to="/">Inicio</RouterLink>
            <RouterLink class="nav-link" :to="{ name: 'home', hash: '#plataforma' }">Plataforma</RouterLink>
            <RouterLink class="nav-link" :to="{ name: 'home', hash: '#contacto' }">Contactenos</RouterLink>
          </template>
        </nav>

        <div class="hidden items-center gap-2 md:flex">
          <template v-if="authStore.isAuthenticated">
            <button class="btn-primary" type="button" @click="handleLogout">Cerrar sesion</button>
          </template>
          <template v-else>
            <RouterLink class="btn-muted hidden sm:inline-flex" to="/login">Login</RouterLink>
            <RouterLink class="btn-primary" to="/register">Crear cuenta</RouterLink>
          </template>
        </div>

        <div class="flex items-center gap-2 md:hidden">
          <button v-if="authStore.isAuthenticated" class="btn-primary px-3 py-2 text-xs" type="button" @click="handleLogout">Cerrar sesion</button>
          <button
            class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-sage bg-white text-forest"
            type="button"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            :aria-expanded="isMobileMenuOpen ? 'true' : 'false'"
            aria-label="Abrir navegacion"
          >
            <span class="text-lg">{{ isMobileMenuOpen ? "×" : "≡" }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="isMobileMenuOpen" class="border-t border-forest/10 bg-white/90 md:hidden">
      <div class="mx-auto flex max-w-6xl flex-col gap-2 px-4 py-4 sm:px-6">
        <template v-if="authStore.isAuthenticated">
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" :to="primaryAuthenticatedRoute" @click="closeMobileMenu">{{ primaryAuthenticatedLabel }}</RouterLink>
          <RouterLink v-if="authStore.hasActiveBaby" class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/eventos" @click="closeMobileMenu">Eventos</RouterLink>
          <RouterLink v-if="authStore.hasActiveBaby" class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/citas" @click="closeMobileMenu">Citas</RouterLink>
          <RouterLink v-if="authStore.hasActiveBaby" class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/crecimiento" @click="closeMobileMenu">Crecimiento</RouterLink>
          <RouterLink v-if="authStore.hasActiveBaby" class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/salud" @click="closeMobileMenu">Salud</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/bebes" @click="closeMobileMenu">Bebes</RouterLink>
        </template>
        <template v-else>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/" @click="closeMobileMenu">Inicio</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" :to="{ name: 'home', hash: '#plataforma' }" @click="closeMobileMenu">Plataforma</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" :to="{ name: 'home', hash: '#contacto' }" @click="closeMobileMenu">Contactenos</RouterLink>
        </template>

        <div class="mt-2 grid gap-2">
          <template v-if="authStore.isAuthenticated">
            <RouterLink class="btn-muted w-full" to="/bebes" @click="closeMobileMenu">Gestionar bebes</RouterLink>
            <button class="btn-primary w-full" type="button" @click="handleLogout">Cerrar sesion</button>
          </template>
          <template v-else>
            <RouterLink class="btn-muted w-full" to="/login" @click="closeMobileMenu">Login</RouterLink>
            <RouterLink class="btn-primary w-full" to="/register" @click="closeMobileMenu">Crear cuenta</RouterLink>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from "vue";
import { useRouter } from "vue-router";

import AppLogo from "./AppLogo.vue";
import { useAuthStore } from "../stores/auth";
import { useToast } from "../composables/toast";

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();
const isMobileMenuOpen = ref(false);

const primaryAuthenticatedRoute = computed(() => {
  return "/dashboard";
});

const primaryAuthenticatedLabel = computed(() => {
  return "Dashboard";
});

function closeMobileMenu() {
  isMobileMenuOpen.value = false;
}

async function handleLogout() {
  closeMobileMenu();
  await authStore.logout();
  toast.info("Sesion cerrada", "Tu sesion fue cerrada correctamente.");
  await router.push("/login");
}
</script>
