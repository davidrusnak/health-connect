<template>
  <i role="img">
    <component :is="icon" class="fill-current" />
  </i>
</template>

<script setup lang="ts">
import { defineAsyncComponent } from "vue";

const props = defineProps<{
  name: string;
  size?: number;
}>();

const icon = defineAsyncComponent(
  () => import(`@/assets/icons/${props.name}.svg`)
);
</script>

<style scoped>
i {
  height: 1.58rem;
  width: 1.58rem;
  line-height: 1em;
  text-align: center;
  display: inline-block;
  position: relative;
  fill: currentColor;
  transform: translateZ(0);
}
</style>
