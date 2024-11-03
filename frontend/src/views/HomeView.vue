<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { RouterLink } from 'vue-router';

const DoctorView = defineAsyncComponent(() => import('@/views/doctor/HomeView.vue'));
const PatientView = defineAsyncComponent(() => import('@/views/patient/HomeView.vue'));
</script>

<template>
    <div class="flex space-x-2 mt-64">
        <RouterLink to="/doktor"><button class="btn-max">
                Pohled doktora
                <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 14 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M1 5h12m0 0L9 1m4 4L9 9" />
                </svg>
            </button></RouterLink>
        <RouterLink to="/pacient">
            <button type="button" class="btn-max">
                Pohled pacienta
                <svg class="rtl:rotate-180 w-3.5 h-3.5 ms-2" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                    fill="none" viewBox="0 0 14 10">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M1 5h12m0 0L9 1m4 4L9 9" />
                </svg>
            </button>
        </RouterLink>
    </div>
</template>

<style scoped>
.btn-max {
    @apply text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800;
    @apply w-96 h-48 text-3xl
}
</style>
