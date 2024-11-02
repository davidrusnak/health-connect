<template>
  Soubor:
  {{ id }}
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import resources from "@/data/library/resources"

const route = useRoute();
const id = route.params.id;
</script>
