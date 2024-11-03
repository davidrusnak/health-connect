<template>
  <div class="max-w-7xl">
    <div class="px-4 py-6 sm:px-0">
        <RequestTable :requests="requests" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const requests = ref([
    {
      "key": 0,
      "patient": "Jana Malá",
      "type": "Prescription",
      "type_label": "Male",
      "timeCreated": "2021-09-14T14:00:00",
      "timeUpdated": "2021-09-14T14:00:00",
      "status": "Pending",
    }
  ]);
</script>