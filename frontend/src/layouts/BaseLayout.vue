<template>
    <div>

    </div>
</template>

<script setup lang="ts">
import { breakpointsTailwind, useBreakpoints } from "@vueuse/core";
import { computed, provide } from "vue";

const breakpoints = useBreakpoints(breakpointsTailwind);
const mobile = computed(() => breakpoints.smallerOrEqual("lg").value);
provide("breakpoints", breakpoints);
provide("isMobile", mobile);
</script>

<style scoped>

</style>