<template>
    <n-button text icon-placement="right">
        <span class="text-md md:text-lg font-semibold">
            {{ label }}
        </span>
        <template #icon>
            <n-icon size="30">
                <slot name="icon"></slot>
            </n-icon>
        </template>
    </n-button>
</template>
  
<script lang="ts" setup>
defineProps<{
  label: string;
}>();
</script>
 