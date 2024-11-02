<template>
  <PatientsTable :patients="patients" />
</template>

<script setup lang="ts">
import { ref } from 'vue';

const patients = ref([
    {
      "name": "Mustafa Abrahim",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Mustafa Abrahim",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Mustafa Abrahim",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Mustafa Abrahim",
      "age": 34,
      "gender": "Male",
      "status": "Approved"
    },
    {
      "name": "Mustafa Abrahim",
      "age": 34,
      "gender": "Male",
      "status": "Pending Sign"
    }
  ]);
</script>