<template>
  <div class="mx-auto grid max-w-5xl gap-6 lg:grid-cols-[0.95fr_1.05fr] lg:gap-8">
    <section class="card order-1 lg:order-2">
      <h1 class="font-display text-3xl font-bold">Iniciar sesión</h1>
      <p class="mt-2 text-sm text-forest/70">Accede a tu cuenta para ver el dashboard de tu bebé.</p>

      <form class="mt-6 space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="label" for="email">Correo</label>
          <input id="email" v-model="form.email" class="input" type="email" required />
        </div>
        <div class="relative">
          <label class="label" for="password">Contraseña</label>
          <input id="password" v-model="form.password" class="input pr-16" :type="showPassword ? 'text' : 'password'" required />
          <button class="password-toggle" type="button" @click="showPassword = !showPassword">
            {{ showPassword ? "Ocultar" : "Ver" }}
          </button>
        </div>

        <div v-if="errorMessage" class="flex items-start space-x-3 rounded-2xl border border-red-200 bg-red-50 p-4">
          <svg class="h-5 w-5 flex-shrink-0 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p class="text-sm font-medium text-red-800">
            {{ errorMessage }}
          </p>
        </div>

        <button class="btn-primary w-full" type="submit" :disabled="authStore.isLoading">
          {{ authStore.isLoading ? "Ingresando..." : "Entrar" }}
        </button>
      </form>

      <p class="mt-4 text-sm text-forest/75">
        ¿Aún no tienes cuenta?
        <RouterLink class="font-semibold text-forest" to="/register">Regístrate</RouterLink>
      </p>
    </section>

    <section class="hero-panel order-2 flex flex-col justify-between px-5 py-6 sm:p-8 lg:order-1">
      <div>
        <span class="section-kicker">Ingreso seguro</span>
        <h2 class="mt-4 font-display text-2xl font-bold text-forest sm:text-4xl">Tu rutina de cuidado, clara desde el primer vistazo</h2>
        <p class="mt-4 text-sm leading-6 text-forest/75">
          Accede a Creciendo para revisar el estado del bebé, seguir citas, crecimiento y notas de salud sin perder tiempo.
        </p>
      </div>

      <div class="mt-6 grid gap-3 sm:mt-8 sm:grid-cols-3">
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Escaneo rápido</p>
          <p class="mt-2 text-sm text-forest/80">Dashboard resumido y legible en segundos.</p>
        </div>
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Calma visual</p>
          <p class="mt-2 text-sm text-forest/80">Paleta suave para una experiencia enfocada y confiable.</p>
        </div>
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Móvil primero</p>
          <p class="mt-2 text-sm text-forest/80">Pensado para registrar datos desde el día a día.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

import { useAuthStore } from "../stores/auth";
import { useToast } from "../composables/toast";

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const form = reactive({
  email: "",
  password: "",
});

const errorMessage = ref("");
const showPassword = ref(false);

async function onSubmit() {
  errorMessage.value = "";
  try {
    await authStore.login(form);
    toast.success("Sesión iniciada", "Bienvenido de vuelta.");
    await router.push("/dashboard");
  } catch (error) {
    errorMessage.value = authStore.normalizeApiError(error, "No fue posible iniciar sesión.");
    toast.error("Error al iniciar sesión", errorMessage.value);
  }
}
</script>