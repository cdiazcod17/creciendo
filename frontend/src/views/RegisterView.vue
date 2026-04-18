<!-- src/views/RegisterView.vue -->
<template>
  <div class="mx-auto grid max-w-5xl gap-6 lg:grid-cols-[0.95fr_1.05fr] lg:gap-8">
    <section class="card order-1 lg:order-2">
      <h1 class="font-display text-3xl font-bold">Crea tu cuenta</h1>
      <p class="mt-2 text-sm text-forest/70">Únete a Creciendo y comienza a monitorear el crecimiento de tu bebé.</p>

      <form class="mt-6 space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="label" for="fullName">Nombre completo</label>
          <input
            id="fullName"
            v-model="form.full_name"
            class="input"
            type="text"
            placeholder="Tu nombre"
            required
          />
        </div>

        <div>
          <label class="label" for="email">Correo</label>
          <input
            id="email"
            v-model="form.email"
            class="input"
            type="email"
            placeholder="tu@email.com"
            required
          />
        </div>

        <div class="relative">
          <label class="label" for="password">Contraseña</label>
          <input
            id="password"
            v-model="form.password"
            class="input pr-16"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Al menos 8 caracteres"
            required
          />
          <button class="password-toggle" type="button" @click="showPassword = !showPassword">
            {{ showPassword ? "Ocultar" : "Ver" }}
          </button>
        </div>

        <div class="relative">
          <label class="label" for="confirmPassword">Confirmar contraseña</label>
          <input
            id="confirmPassword"
            v-model="form.confirm_password"
            class="input pr-16"
            :type="showConfirmPassword ? 'text' : 'password'"
            placeholder="Repite tu contraseña"
            required
          />
          <button class="password-toggle" type="button" @click="showConfirmPassword = !showConfirmPassword">
            {{ showConfirmPassword ? "Ocultar" : "Ver" }}
          </button>
        </div>

        <p v-if="errorMessage" class="rounded-xl border border-red-300 bg-red-50 px-3 py-2 text-sm text-red-700">
          {{ errorMessage }}
        </p>

        <button class="btn-primary w-full" type="submit" :disabled="authStore.isLoading">
          {{ authStore.isLoading ? "Registrando..." : "Registrarme" }}
        </button>
      </form>

      <p class="mt-4 text-sm text-forest/75">
        ¿Ya tienes cuenta?
        <RouterLink class="font-semibold text-forest" to="/login">Inicia sesión</RouterLink>
      </p>
    </section>

    <section class="hero-panel order-2 flex flex-col justify-between px-5 py-6 sm:p-8 lg:order-1">
      <div>
        <span class="section-kicker">Bienvenido a Creciendo</span>
        <h2 class="mt-4 font-display text-2xl font-bold text-forest sm:text-4xl">Registra tu bebé y comienza hoy</h2>
        <p class="mt-4 text-sm leading-6 text-forest/75">
          Creciendo te ayuda a mantener un seguimiento completo del desarrollo, salud y cuidados de tu bebé en un solo lugar seguro y fácil de usar.
        </p>
      </div>

      <div class="mt-6 grid gap-3 sm:mt-8 sm:grid-cols-3">
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Registro seguro</p>
          <p class="mt-2 text-sm text-forest/80">Tus datos están encriptados y protegidos.</p>
        </div>
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Acceso inmediato</p>
          <p class="mt-2 text-sm text-forest/80">Comienza a registrar datos en segundos.</p>
        </div>
        <div class="rounded-2xl bg-white/70 p-4">
          <p class="text-xs uppercase tracking-widest text-forest/50">Sin compromisos</p>
          <p class="mt-2 text-sm text-forest/80">Cancela cuando quieras sin penalidades.</p>
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
  full_name: "",
  email: "",
  password: "",
  confirm_password: "",
});

const errorMessage = ref("");
const showPassword = ref(false);
const showConfirmPassword = ref(false);

async function onSubmit() {
  errorMessage.value = "";

  if (form.password !== form.confirm_password) {
    errorMessage.value = "Las contraseñas no coinciden";
    return;
  }

  if (form.password.length < 8) {
    errorMessage.value = "La contraseña debe tener al menos 8 caracteres";
    return;
  }

  try {
    await authStore.register({
      full_name: form.full_name,
      email: form.email,
      password: form.password,
    });
    toast.success("¡Bienvenido!", "Tu cuenta ha sido creada exitosamente.");
    await router.push("/dashboard");
  } catch (error) {
    errorMessage.value = authStore.normalizeApiError(error, "No fue posible crear tu cuenta.");
    toast.error("Error al registrarse", errorMessage.value);
  }
}
</script>