<template>
  <div class="flex flex-col space-y-3 lg:space-y-4 xl:max-w-7xl w-full">
    <div class="item-start w-full">
      <EduResourceList :resources="resources" class="relative pb-8" @open="openResource" />
    </div>
    <n-button type="primary" class="max-w-lg" @click="createNew">Vytvořit nový</n-button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import resources from "@/data/library/resources"
import router from "@/router";
import type { EduResource } from "@/data/library";

function openResource(doc: EduResource) {
  router.push({ name: 'doctor-edu-resource-reader', params: { id: doc.fileId } });
}

function createNew() {
  // TODO: call backend to create new doc

  router.push({ name: 'doctor-edu-resource-edit', params: { id: '1' } });
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