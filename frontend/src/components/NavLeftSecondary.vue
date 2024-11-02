<template>
    <div>
        <div class="fixed bottom-8 left-0 right-0 w-2/3 xl:w-full max-w-fit">
      <div class="mt-12 ml-5">
        <h3
          class="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider"
          id="projects-headline"
        >
          O aplikaci
        </h3>
        <div class="space-y-1">
          <a
            v-for="item in secondaryNavigation"
            :key="item.name"
            :href="item.href"
            class="group flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:text-gray-900 hover:bg-gray-50"
          >
            <span class="truncate">
              {{ item.name }}
            </span>
          </a>
        </div>
      </div>
    </div>
    </div>
</template>

<script setup lang="ts">
const secondaryNavigation = [
  { name: "Informace o výzkumu", href: "#" },
  { name: "Umělá inteligence", href: "#" },
  { name: "Zpětná vazba", href: "#" },
];
</script>

<style scoped>

</style>