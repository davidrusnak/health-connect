<template>
  <div v-once class="sentry-unmask flex flex-col space-y-4 md:space-y-8 max-w-3xl pb-4 sm:pb-8" :class="{'mx-3': mobile}">
    <section class="max-w-prose flex flex-col lg:flex-row lg:space-x-12">
      <p>
        Umožňujeme vám dělat informovaná rozhodnutí o svém zdraví s ohledem na vaše individuální potřeby a cíle.
      </p>
    </section>

    <section class="max-w-prose">
      <h2>Co vše zde můžete dělat?</h2>
      <HomeActions />
    </section>

    <section>
      <h2 class="pt-2">Jak začít?</h2>
      <p>Prohlédněte si svou <RouterLink :to="{ name: 'health-records' }" class="link">poslední lékařskou zprávu</RouterLink>.</p>
    </section>

  </div>
</template>

<script setup lang="ts">
import { inject } from "vue";

const mobile = inject('mobile');
</script>

<style scoped>
p {
  @apply mb-0;
}
</style>
