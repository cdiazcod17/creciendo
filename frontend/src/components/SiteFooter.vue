<template>
  <footer class="mt-10 border-t border-forest/10 bg-white/40">
    <div class="mx-auto grid max-w-6xl gap-8 px-4 py-8 sm:px-6 lg:grid-cols-[1.1fr_0.9fr_0.9fr] lg:px-8 lg:py-10">
      <div>
        <AppLogo />
        <p class="mt-4 max-w-md text-sm leading-6 text-forest/70">
          Creciendo acompaña a los padres primerizos a cuidar de su bebe con una plataforma clara, confiable  y facil de usar.
        </p>
      </div>

      <div>
        <p class="text-sm font-semibold text-forest">Navegacion</p>
        <div class="mt-4 flex flex-col gap-2 text-sm text-forest/70">
          <RouterLink to="/">Inicio</RouterLink>
          <RouterLink to="/home#plataforma">Plataforma</RouterLink>
          <RouterLink to="/home#contacto">Contactenos</RouterLink>
        </div>
      </div>

      <div>
        <p class="text-sm font-semibold text-forest">Contacto</p>
        <div class="mt-4 space-y-2 text-sm text-forest/70">
          <p>hola@creciendo.app</p>
          <p>Soporte, pruebas y mejoras.</p>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import AppLogo from "./AppLogo.vue";
</script>
