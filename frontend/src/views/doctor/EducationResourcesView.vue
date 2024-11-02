<template>
  <div class="flex flex-col space-y-3 lg:space-y-4 xl:max-w-7xl w-full">
    <div class="item-start w-full">
      <InfolibDocumentList :documents="resources" class="relative pb-8" @open="openResource" />
    </div>
    <n-button type="primary" class="max-w-lg" @click="createNew">Vytvořit nový</n-button>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import resources from "@/data/library/resources"
import router from "@/router";
import type { EducationResource } from "@/data/library";

function openResource(doc: EducationResource) {
  router.push({ name: 'doctor-education-resource-reader', params: { id: doc.fileId } });
}

function createNew() {
  // TODO: call backend to create new doc

  router.push({ name: 'doctor-education-resource-edit', params: { id: '2' } });
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