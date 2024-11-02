<script setup lang="ts">
import { provide, ref } from 'vue';
import { RouterView } from 'vue-router'
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import { useOptionsStore } from '@/stores/options';
import * as themeOverrides from "@/assets/naive-ui-theme-overrides.json";

const mobile = ref(useBreakpoints(breakpointsTailwind).smallerOrEqual("lg"));
provide("mobile", mobile);

const optionsStore = useOptionsStore();
provide("userRole", optionsStore.userRole);
</script>

<template>
  <n-config-provider :theme-overrides="themeOverrides">
    <n-global-style />
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-message-provider>
          <Suspense><router-view /></Suspense>
        </n-message-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<style scoped></style>
