<template>
  <header class="sticky top-0 left-0 right-0 text-xs leading-tight h-fit z-10 transition-shadow ease-in-out"
    :class="{ 'shadow-lg lg:shadow-none': shadow }">
    <div class="flex flex-wrap justify-between items-center px-3 xl:px-7 py-2 lg:py-4" 
        :class="{'bg-aic-bg': background === 'white', 'lg:bg-transparent': background === 'lg:transparent', 'bg-aic-bg-rose': background === 'rose' }" v-auto-animate>
      <div class="flex flex-row"><slot name="left" />
      <div class="flex flex-row space-x-1 items-center min-w-fit">
        <h1 class="flex flex-col space-y-4 pl-0.5 md:pl-4 xl:pl-0.5">
          <a v-if="!inDeeperPage" @click="emit('clickLogo')" class="flex flex-row items-center space-x-3">
            <img src="/logo-icon.svg" class="w-12 md:w-16 lg:w-24 mt-0.5" />
            <span v-if="pageTitle && !hidePageTitle" class="font-bold text-lg sm:text-xl md:text-2xl">{{
              pageTitle
            }}</span>
            <span v-else class="cursor-pointer w-max font-bold text-xl md:text-2xl relative right-0.5 top-0.5" :class="{'opacity-0 xl:opacity-1000 transition-opacity duration-200': hidePageTitle}">
              HealthConnect
            </span>
          </a>
          <span v-else class="font-bold text-lg sm:text-xl md:text-2xl mt-1 ml-2">{{ pageTitle }}</span>
        </h1>
      </div></div>

      <div class="flex flex-shrink-0 space-x-3 py-6">
        <slot name="center" />
        <!-- <SearchBar /> -->
      </div>

      <div class="flex flex-row space-x-12">
        <slot name="right0"></slot>
        <div class="flex flex-row space-x-2">
          <template v-if="!hidePageTitle"><slot name="right"></slot></template>
          <div class="flex justify-items-stretch h-auto flex-col-reverse items-center">
            <slot name="right2"></slot>
            <div>
              <LogoutButton v-if="showDefaultLogout" @click="emit('clickLogout')" />
            </div>
          </div>
         </div>
      </div>
    </div>

    <div class="">
      <slot name="progress" />
    </div>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  mobile?: boolean;
  pageTitle?: string;
  btnTitle?: string;
  shadow?: boolean;
  admin?: boolean;
  background?: "white" | "lg:transparent" | "rose";
  showDefaultLogout?: boolean;
  hidePageTitle?: boolean;
  inDeeperPage?: boolean;
}>();

const emit = defineEmits<{
  clickLogo: [];
  clickLogout: [];
}>();
</script>

<style scoped>
a {
  text-decoration: none;
  color: inherit;
}
</style>
