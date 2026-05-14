<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-[60] flex items-center justify-center bg-forest/30 p-4 sm:p-6">
      <div class="flex h-full max-h-[85vh] w-full max-w-2xl flex-col rounded-3xl border border-sage bg-white shadow-xl">
        <!-- Header -->
        <div class="border-b border-sage/30 px-6 py-4">
          <p class="text-xs font-semibold uppercase tracking-[0.2em] text-forest/55">Legal</p>
          <h3 class="font-display text-xl font-semibold text-forest">Términos y Privacidad</h3>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto p-6 text-sm text-forest/80 leading-relaxed">
          <section class="space-y-6">
            <div>
              <h4 class="text-base font-bold text-forest uppercase tracking-wider">Términos y Condiciones</h4>
              <p class="mt-2 text-xs text-forest/50">Última actualización: 5 de mayo de 2026</p>
              
              <div class="mt-4 space-y-4">
                <p><strong>1. Aceptación de los Términos:</strong> Al acceder y utilizar Creciendo, usted acepta estar sujeto a estos Términos y Condiciones. Si no está de acuerdo con alguna parte de estos términos, no podrá utilizar nuestro servicio.</p>
                <p><strong>2. Descripción del Servicio:</strong> Creciendo es una plataforma diseñada para ayudar a padres y cuidadores a realizar un seguimiento del crecimiento, salud y rutinas de sus bebés. El servicio se proporciona "tal cual" y "según disponibilidad".</p>
                <p><strong>3. Responsabilidad del Usuario:</strong> Usted es responsable de mantener la confidencialidad de su cuenta y contraseña. También es responsable de la exactitud de los datos que ingresa en la plataforma.</p>
                <p class="rounded-xl bg-leaf/10 p-4 font-semibold text-forest"><strong>4. Uso Médico (IMPORTANTE):</strong> Creciendo NO proporciona asesoramiento médico profesional. La información registrada y mostrada en la aplicación es solo para fines informativos y de seguimiento personal. Siempre consulte con un pediatra o profesional de la salud calificado para cualquier duda sobre la salud de su bebé.</p>
                <p><strong>5. Modificaciones:</strong> Nos reservamos el derecho de modificar estos términos en cualquier momento. Los cambios entrarán en vigor inmediatamente después de su publicación en esta página.</p>
                <p><strong>6. Contacto:</strong> Si tiene alguna pregunta sobre estos Términos, por favor contáctenos en hola@creciendo.app.</p>
              </div>
            </div>

            <div class="border-t border-sage/30 pt-6">
              <h4 class="text-base font-bold text-forest uppercase tracking-wider">Política de Privacidad</h4>
              
              <div class="mt-4 space-y-4">
                <p><strong>1. Información que Recopilamos:</strong> Recopilamos información que usted nos proporciona directamente al crear una cuenta y al utilizar la aplicación, incluyendo nombre, correo electrónico, datos de sus bebés (nombre, fecha de nacimiento, sexo), registros de crecimiento y eventos diarios.</p>
                <p><strong>2. Uso de la Información:</strong> Utilizamos la información recopilada para proporcionar y mantener el servicio, personalizar su experiencia y mejorar nuestra plataforma.</p>
                <p><strong>3. Seguridad de los Datos:</strong> La seguridad de sus datos es nuestra prioridad. Implementamos medidas técnicas y organizativas para proteger su información personal.</p>
                <p><strong>4. Sus Derechos:</strong> Usted tiene derecho a acceder, rectificar o eliminar sus datos personales en cualquier momento a través de la configuración de su cuenta.</p>
                <p><strong>5. Cookies:</strong> Utilizamos cookies para mantener su sesión activa y recordar sus preferencias.</p>
                <p><strong>6. Contacto:</strong> Para cualquier duda sobre esta Política de Privacidad, escríbanos a hola@creciendo.app.</p>
              </div>
            </div>
          </section>
        </div>

        <!-- Footer -->
        <div class="border-t border-sage/30 p-5 sm:p-6">
          <div class="grid gap-2 sm:grid-cols-2">
            <button class="btn-muted w-full" type="button" @click="$emit('close')">
              Cerrar
            </button>
            <button class="btn-primary w-full" type="button" @click="$emit('accept')">
              Leer y Aceptar
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
defineProps({
  open: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["close", "accept"]);
</script>
