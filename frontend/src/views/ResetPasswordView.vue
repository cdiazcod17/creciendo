<template>
  <div class="mx-auto max-w-md py-12">
    <section class="card">
      <h1 class="font-display text-3xl font-bold">Nueva contraseña</h1>
      <p class="mt-2 text-sm text-forest/70">Establece tu nueva contraseña de acceso.</p>

      <form class="mt-6 space-y-4" @submit.prevent="onSubmit">
        <div class="relative">
          <label class="label" for="password">Nueva contraseña</label>
          <input id="password" v-model="form.new_password" class="input pr-16" :type="showPassword ? 'text' : 'password'" required minlength="8" />
          <button class="password-toggle" type="button" @click="showPassword = !showPassword">
            {{ showPassword ? "Ocultar" : "Ver" }}
          </button>
        </div>

        <div class="relative">
          <label class="label" for="confirm_password">Confirmar contraseña</label>
          <input id="confirm_password" v-model="form.confirm_password" class="input" :type="showPassword ? 'text' : 'password'" required />
        </div>

        <div v-if="errorMsg" class="rounded-xl bg-red-50 p-4 text-sm text-red-800 border border-red-100">
          {{ errorMsg }}
        </div>

        <button class="btn-primary w-full" type="submit" :disabled="isLoading">
          {{ isLoading ? "Actualizando..." : "Cambiar contraseña" }}
        </button>
      </form>
    </section>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { authApi } from "../services/auth";
import { useToast } from "../composables/toast";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const isLoading = ref(false);
const showPassword = ref(false);
const errorMsg = ref("");
const token = ref("");

const form = reactive({
  new_password: "",
  confirm_password: "",
});

onMounted(() => {
  token.value = route.query.token;
  if (!token.value) {
    toast.error("Error", "El enlace es inválido o ha expirado.");
    router.push("/login");
  }
});

async function onSubmit() {
  if (form.new_password !== form.confirm_password) {
    errorMsg.value = "Las contraseñas no coinciden.";
    return;
  }

  errorMsg.value = "";
  isLoading.value = true;

  try {
    await authApi.resetPassword({
      token: token.value,
      new_password: form.new_password,
    });
    toast.success("¡Éxito!", "Tu contraseña ha sido actualizada.");
    router.push("/login");
  } catch (error) {
    errorMsg.value = error.response?.data?.detail || "No se pudo actualizar la contraseña.";
    toast.error("Error", errorMsg.value);
  } finally {
    isLoading.value = false;
  }
}
</script>
