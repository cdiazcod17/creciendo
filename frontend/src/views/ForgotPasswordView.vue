<template>
  <div class="mx-auto max-w-md py-12">
    <section class="card">
      <h1 class="font-display text-3xl font-bold">Recuperar contraseña</h1>
      <p class="mt-2 text-sm text-forest/70">
        Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
      </p>

      <form v-if="!submitted" class="mt-6 space-y-4" @submit.prevent="onSubmit">
        <div>
          <label class="label" for="email">Correo</label>
          <input id="email" v-model="email" class="input" type="email" required placeholder="tu@email.com" />
        </div>

        <button class="btn-primary w-full" type="submit" :disabled="isLoading">
          {{ isLoading ? "Enviando..." : "Enviar enlace" }}
        </button>

        <p class="mt-4 text-center text-sm">
          <RouterLink class="font-semibold text-forest" to="/login">Volver al inicio de sesión</RouterLink>
        </p>
      </form>

      <div v-else class="mt-6 text-center">
        <div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-green-600">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <p class="text-forest font-medium">¡Enlace enviado!</p>
        <p class="mt-2 text-sm text-forest/70">
          Si el correo está registrado, recibirás un mensaje en unos minutos. Revisa también tu carpeta de spam.
        </p>
        <button class="btn-primary mt-6 w-full" @click="submitted = false">Reintentar con otro correo</button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { authApi } from "../services/auth";
import { useToast } from "../composables/toast";

const toast = useToast();
const email = ref("");
const isLoading = ref(false);
const submitted = ref(false);

async function onSubmit() {
  isLoading.value = true;
  try {
    await authApi.forgotPassword(email.value);
    submitted.value = true;
    toast.success("Correo enviado", "Revisa tu bandeja de entrada.");
  } catch (error) {
    const msg = error.response?.data?.detail || "No se pudo procesar la solicitud.";
    toast.error("Error", msg);
  } finally {
    isLoading.value = false;
  }
}
</script>
