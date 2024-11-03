<template>
  <div class="max-w-full grid gap-3 lg:max-w-none mobile-grid-x"
    style="grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));" v-auto-animate>
    <template v-for="d in resources" :key="d.title">
      <EduResourceCard :d="d" @click-content="emit('open', d)" />
    </template>
    <div class="flex flex-col items-start justify-center">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { EduResource } from "@/data/library"
import { ref } from "vue";

defineProps<{
  resources: EduResource[];
}>();

const emit = defineEmits<{
  open: [brochure: any];
}>();
</script>

<style scoped>
.mobile-grid-x {
  overflow-x: auto;
  /* Enable horizontal scrolling */
  scroll-snap-type: x mandatory;
  /* Snap to the start of each card */
}

@media (max-width: 767px) {
  .mobile-grid-x {
    grid-template-columns: auto;
    /* Reset the column layout for smaller screens */
    width: 100%;
    /* Ensure the grid fits the screen width */
  }
}
</style>