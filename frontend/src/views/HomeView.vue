<script setup lang="ts">
import { defineAsyncComponent } from 'vue';
import { RouterLink } from 'vue-router';

const DoctorView = defineAsyncComponent(() => import('@/views/doctor/HomeView.vue'));
const PatientView = defineAsyncComponent(() => import('@/views/patient/HomeView.vue'));
</script>

<template>
    <div class="flex justify-center items-center space-x-2 mt-64">
        <n-button primary>
            <RouterLink to="/doktor">Pohled doktora</RouterLink>
        </n-button>
        <n-button primary>
            <RouterLink to="/pacient">Pohled pacienta</RouterLink>
        </n-button>
    </div>
</template>
