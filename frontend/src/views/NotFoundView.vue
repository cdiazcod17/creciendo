<template>
  <div class="min-h-[calc(100vh-5rem)] flex flex-col items-center justify-center px-6 py-12 text-center">
    <div class="max-w-lg rounded-[2rem] border border-sage bg-white/95 p-10 shadow-xl">
      <img class="rounded" src="https://img.freepik.com/vector-gratis/lindo-nino-llorando-icono-vectorial-dibujos-animados-ilustracion-personas-icono-naturaleza-vector-plano-aislado_138676-11870.jpg?semt=ais_hybrid&w=740&q=80" alt="">
      <p class="text-xs font-semibold uppercase tracking-[0.24em] text-forest/60">404</p>
      <h1 class="mt-4 text-4xl font-bold text-forest">Página no encontrada</h1>
      <p class="mt-4 text-sm leading-6 text-forest/75">
        La ruta que buscabas no existe o ya no está disponible. Regresa al inicio para iniciar sesión.
      </p>
      <div class="mt-8 flex justify-center gap-3">
        <RouterLink to="/" class="btn-primary">Regresar</RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
