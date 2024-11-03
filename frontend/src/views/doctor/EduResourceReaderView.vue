<template>
  <div class="flex flex-col max-w-6xl">
    <h2>{{ resource.title }}</h2>
    <div class="flex flex-row items-stretch space-x-8 justify-items-stretch justify-between">
      <div class="rounded-4 p-4 bg-slate-100">
        <n-descriptions label-placement="top" title="Metadata">
          <n-descriptions-item>
            <template #label>
              Autor
            </template>
            MUDr. Eva Hlanská
          </n-descriptions-item>
        </n-descriptions>
      </div>
      <div class="space-x-4">
        <n-button type="secondary">Přiradit pacientovi</n-button>
        <n-button type="primary"
          @click="router.push({ name: 'doctor-edu-resource-edit', params: { id: 1 } })">Editovat</n-button>
      </div>
    </div>
  </div>
  <div class="max-w-6xl my-8">
    <Card>
      <div v-if="id === '1'" v-html="example" class="m-8 mt-12"></div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import resources from "@/data/library/resources"
import example from "@/data/library/example"

const route = useRoute();
const router = useRouter();
const id = route.params.id;

const resource = resources.find((r) => r.fileId === id);
</script>
