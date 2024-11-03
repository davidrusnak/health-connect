<template>
    <div class="flex flex-col max-w-6xl">
      <h2>{{ resource.title }}</h2>
      <h5>MUDr. Eva Hlanská</h5>
      <div class="max-w-6xl my-8">
        <Card>
          <div v-if="id === '1'" v-html="example" class="m-8 mt-12"></div>
        </Card>
      </div>
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
  