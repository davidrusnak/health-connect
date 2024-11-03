<template>
  <div v-once class="sentry-unmask flex flex-col space-y-4 md:space-y-8 max-w-3xl pb-4 sm:pb-8" :class="{'mx-3': mobile}">
    <section class="max-w-prose flex flex-col lg:flex-row lg:space-x-12">
      <h4>Nadcházející schůzky</h4>
      <p>
        <span class="font-bold">Dnes</span>
        <br />
        <span>14:00 - 14:30</span>
        <br />
        <span>Dr. Novák</span>
      </p>
    </section>

    <section>
      <h4>Na vyplnění</h4>
      <p>
        <span class="font-bold">Dokončit dotazník</span>
        <br />
        <span>do 15. 9. 2021</span>
      </p>
    </section>

    <section>
      <h4>Poslední výsledky</h4>
      <p>
        <span class="font-bold">Krevní obraz</span>
        <br />
        <span>12. 9. 2021</span>
      </p>
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
