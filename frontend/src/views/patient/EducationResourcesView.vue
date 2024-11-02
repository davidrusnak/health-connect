<template>
  <div class="flex flex-col space-y-3 lg:space-y-4 xl:max-w-7xl w-full">
    <div class="item-start w-full">
      <InfolibDocumentList :documents="brochures" class="relative pb-8" @open="openDocument" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import brochures from "@/data/library/brochures"
import router from "@/router";
import type { InfolibDocument } from "@/data/library";

function openDocument(doc: InfolibDocument) {
  router.push({ name: 'doctor-education-material-editor', params: { fileId: doc.fileId } });
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