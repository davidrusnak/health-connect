<script lang="ts" setup>
defineProps<{
    label: string;
    back: boolean;
}>();
</script>

<template>
    <template v-if="back">
        <button class="btn-max !bg-slate-400 hover:!bg-slate-600">
            <svg class="w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" style="transform: rotate(180deg);" 
                viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5h12m0 0L9 1m4 4L9 9" />
            </svg>
            {{ label ?? 'Zpět' }}
        </button>
    </template>
    <template v-else>
        <button class="btn-max">
            {{ label }}
            <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 14 10">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M1 5h12m0 0L9 1m4 4L9 9" />
            </svg>
        </button>
    </template>
</template>

<style scoped>
.btn-max {
    @apply text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800;
    @apply w-full lg:w-80 h-20 lg:h-24 text-lg;
}
</style>
