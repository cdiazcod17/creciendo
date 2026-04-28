<template>
  <header class="sticky top-0 z-40 border-b border-forest/10 bg-paper/85 backdrop-blur">
    <div class="mx-auto max-w-6xl px-4 py-3 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between gap-3">
        <AppLogo />

        <nav class="hidden items-center gap-6 md:flex">
          <template v-if="authStore.isAuthenticated">
            <RouterLink class="nav-link" :to="primaryAuthenticatedRoute">{{ primaryAuthenticatedLabel }}</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/eventos">Eventos</RouterLink>
            <RouterLink v-if="authStore.hasActiveBaby" class="nav-link" to="/appointments">Citas</RouterLink>
            <RouterLink class="nav-link" to="/babies">Bebés</RouterLink>
            <div v-if="babiesStore.activeBaby" class="ml-2 flex items-center gap-2 rounded-full bg-leaf/10 px-3 py-1 text-xs font-medium text-leaf">
              <span class="h-1.5 w-1.5 rounded-full bg-leaf animate-pulse"></span>
              {{ babiesStore.activeBaby.name }}
            </div>
          </template>
          <template v-else>
            <RouterLink class="nav-link" to="/home">Inicio</RouterLink>
            <RouterLink class="nav-link" :to="{ name: 'home', hash: '#plataforma' }">Plataforma</RouterLink>
            <RouterLink class="nav-link" :to="{ name: 'home', hash: '#contacto' }">Contáctenos</RouterLink>
          </template>
        </nav>

        <div class="hidden items-center gap-2 md:flex">
          <template v-if="authStore.isAuthenticated">
            <button class="btn-primary" type="button" @click="handleLogout">Cerrar sesión</button>
          </template>
          <template v-else>
            <RouterLink class="btn-muted hidden sm:inline-flex" to="/login">Login</RouterLink>
            <RouterLink class="btn-primary" to="/register">Crear cuenta</RouterLink>
          </template>
        </div>

        <div class="flex items-center gap-2 md:hidden">
          <button v-if="authStore.isAuthenticated" class="btn-primary px-3 py-2 text-xs" type="button" @click="handleLogout">Cerrar sesión</button>
          <button
            class="inline-flex h-10 w-10 items-center justify-center rounded-xl border border-sage bg-white text-forest"
            type="button"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            :aria-expanded="isMobileMenuOpen ? 'true' : 'false'"
            aria-label="Abrir navegación"
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
          <RouterLink v-if="authStore.hasActiveBaby" class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/appointments" @click="closeMobileMenu">Citas</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/babies" @click="closeMobileMenu">Bebés</RouterLink>
          <div v-if="babiesStore.activeBaby" class="mt-1 flex items-center gap-2 rounded-xl bg-leaf/10 px-3 py-2 text-sm font-medium text-leaf">
            <span class="h-1.5 w-1.5 rounded-full bg-leaf animate-pulse"></span>
            Bebé activo: {{ babiesStore.activeBaby.name }}
          </div>
        </template>
        <template v-else>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" to="/" @click="closeMobileMenu">Inicio</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" :to="{ name: 'home', hash: '#plataforma' }" @click="closeMobileMenu">Plataforma</RouterLink>
          <RouterLink class="nav-link rounded-xl px-2 py-2 hover:bg-mist" :to="{ name: 'home', hash: '#contacto' }" @click="closeMobileMenu">Contáctenos</RouterLink>
        </template>

        <div class="mt-2 grid gap-2">
          <template v-if="authStore.isAuthenticated">
            <RouterLink class="btn-muted w-full" to="/babies" @click="closeMobileMenu">Gestionar bebés</RouterLink>
            <button class="btn-primary w-full" type="button" @click="handleLogout">Cerrar sesión</button>
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
import { useBabiesStore } from "../stores/babies";
import { useToast } from "../composables/toast";

const router = useRouter();
const authStore = useAuthStore();
const babiesStore = useBabiesStore();
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
  toast.info("Sesión cerrada", "Tu sesión fue cerrada correctamente.");
  await router.push("/login");
}
</script>
