<template>
  <div class="max-w-7xl">
    <div class="px-4 py-6 sm:px-0">
        <PatientsTable :patients="patients" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const patients = ref([
    {
      "name": "Jana Malá",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Jana Malá",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Jana Malá",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Jana Malá",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Jana Malá",
      "age": 34,
      "gender": "Male",
      "status": "Pending Sign"
    }
  ]);
</script>