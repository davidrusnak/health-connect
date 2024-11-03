<template>
  <h2>Tyto materiály Vám doporučuje číst váš lékař:</h2>
  <div class="flex flex-col space-y-3 lg:space-y-4 xl:max-w-7xl w-full">
    <div class="item-start w-full">
      <EduResourceList :resources="resources" class="relative pb-8" @open="openResource" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import resources from "@/data/library/resources"
import router from "@/router";
import type { EduResource } from "@/data/library";

function openResource(doc: EduResource) {
  router.push({ name: 'patient-edu-resource-reader', params: { id: doc.fileId } });
}
</script>

<style scoped>
.n-button__content {
  @apply w-auto min-w-fit;
}

.filterSelect>.n-button {
  @apply !w-fit;
}
</style>