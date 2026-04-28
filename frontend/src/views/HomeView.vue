<template>
  <div class="mx-auto max-w-6xl space-y-10 px-4 pb-6 sm:px-6 sm:space-y-12 sm:pb-8">
    <section class="grid gap-6 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:gap-8">
      <div class="hero-panel px-5 py-6 sm:p-8">
        <span class="section-kicker">Cuidado con amor</span>
        <h1 class="mt-4 max-w-2xl font-display text-3xl font-bold leading-tight text-forest sm:mt-5 sm:text-5xl">
          Una plataforma simple para seguir la salud y rutina de tus bebés.
        </h1>
        <p class="mt-4 max-w-xl text-sm leading-7 text-forest/75 sm:mt-5 sm:text-base">
          Creciendo organiza tu día a día con el bebé.
        </p>

        <div class="mt-8 flex flex-col gap-3 sm:flex-row">
          <RouterLink v-if="!authStore.isAuthenticated" class="btn-primary" to="/register">Empezar ahora</RouterLink>
          <RouterLink v-else class="btn-primary" to="/dashboard">Continuar</RouterLink>
          <RouterLink class="btn-muted" to="/home#plataforma">Conocer la plataforma</RouterLink>
        </div>
      </div>

      <div class="grid gap-4">
        <article class="card bg-white/90">
          <p class="text-xs uppercase tracking-widest text-forest/50">Dashboard útil</p>
          <h2 class="mt-2 font-display text-2xl font-semibold text-forest">Información clave en pocos segundos</h2>
          <p class="mt-3 text-sm leading-6 text-forest/72">
            Vista pensada para madres, padres y cuidadores que necesitan ubicar rápidamente el estado actual del bebé sin navegar demasiadas pantallas.
          </p>
        </article>
        <article class="grid gap-4 sm:grid-cols-2">
          <div class="card">
            <p class="text-xs uppercase tracking-widest text-forest/50">Personal</p>
            <p class="mt-2 text-sm text-forest/75">Puedes hacer el registro de todos tus bebés.</p>
          </div>
          <div class="card">
            <p class="text-xs uppercase tracking-widest text-forest/50">Llévalo a todo lugar</p>
            <p class="mt-2 text-sm text-forest/75">Diseño móvil para que la puedas usar en cualquier lugar.</p>
          </div>
        </article>
      </div>
    </section>

    <section id="plataforma" class="space-y-5">
      <div>
        <span class="section-kicker">Plataforma</span>
        <h2 class="mt-4 font-display text-2xl font-semibold text-forest sm:text-3xl">Qué puedes hacer en Creciendo</h2>
      </div>

      <div class="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <article class="card">
          <p class="text-sm font-semibold text-forest">Eventos diarios</p>
          <p class="mt-2 text-sm text-forest/72">Lactancia, sueño, cambios de pañal y cualquier rutina clave en un historial ordenado.</p>
        </article>
        <article class="card">
          <p class="text-sm font-semibold text-forest">Citas y seguimiento</p>
          <p class="mt-2 text-sm text-forest/72">Consultas, vacunas y controles médicos visibles desde el dashboard.</p>
        </article>
        <article class="card">
          <p class="text-sm font-semibold text-forest">Crecimiento</p>
          <p class="mt-2 text-sm text-forest/72">Peso, talla y medidas para mantener una evolución legible y consistente.</p>
        </article>
        <article class="card">
          <p class="text-sm font-semibold text-forest">Notas de salud</p>
          <p class="mt-2 text-sm text-forest/72">Síntomas, medicamentos y observaciones almacenadas en un mismo lugar.</p>
        </article>
      </div>
    </section>

    <section id="contacto" class="grid gap-4 lg:grid-cols-[1fr_0.9fr]">
      <article class="hero-panel px-5 py-6 sm:p-8">
        <span class="section-kicker">Contáctenos</span>
        <h2 class="mt-4 font-display text-2xl font-semibold text-forest sm:text-3xl">Estamos construyendo una herramienta con cuidado y útil</h2>
        <p class="mt-4 max-w-xl text-sm leading-6 text-forest/75">
          Si quieres compartir feedback, solicitar una demo o revisar prioridades del producto, podemos conversar sobre el flujo ideal para familias y cuidadores.
        </p>
      </article>

      <article class="card">
        <p class="text-sm font-semibold text-forest">Canales</p>
        <div class="mt-4 space-y-3 text-sm text-forest/75">
          <p><strong>Email:</strong> hola@creciendo.app</p>
          <p><strong>Enfoque:</strong> producto, soporte y mejoras.</p>
        </div>
        <div class="mt-6 flex flex-col gap-3 sm:flex-row">
          <template v-if="!authStore.isAuthenticated">
            <RouterLink class="btn-primary" to="/register">Crear una cuenta</RouterLink>
            <RouterLink class="btn-muted" to="/login">Ya tengo acceso</RouterLink>
          </template>
          <template v-else>
            <RouterLink class="btn-primary" to="/dashboard">Ir a mi espacio</RouterLink>
          </template>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";

const authStore = useAuthStore();
</script>