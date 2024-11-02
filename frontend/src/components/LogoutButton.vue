<template>
  <n-button text icon-placement="right">
    <span class="text-md md:text-lg font-semibold">odhlášení</span>
    <template #icon>
      <n-icon size="30">
        <log-out-outline />
      </n-icon>
    </template>
  </n-button>
</template>

<script lang="ts" setup>
import { LogOutOutline } from "@vicons/ionicons5";
</script>

<style scoped></style>