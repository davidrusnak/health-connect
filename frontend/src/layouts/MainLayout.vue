<template>
  <!-- 
    MOBILE 
  -->
  <template v-if="mobile">
    <Header @clickLogo="router.push({ name: 'doctor-home' })" :shadow="y > 20" :admin="isDoctor" class="select-none"
      :page-title="route.name?.toString() == default_route_name ? 'HealthConnect' : route.meta?.headline"
      background="white" :inDeeperPage="!!route?.meta?.parentName">
      <template #left>
        <template v-if="route?.meta?.parentName">
          <RouterLink :to="{ name: route.meta.parentName }"><n-icon size="32" class="relative top-1">
              <ChevronBack />
            </n-icon></RouterLink>
        </template>
      </template>
      <template #right2>
        <div class="flex flex-row space-x-6" v-if="!route.meta?.public">
          <NavLeftPrimary mobile>
            <template #menuDrawer>
              <n-button type="primary" icon-placement="right" id="btn-logout">
                <span class="text-lg md:text-xl font-semibold mr-2">{{
    "odhlášení"
  }}</span>
                <template #icon>
                  <n-icon size="30">
                    <log-out-outline />
                  </n-icon>
                </template>
              </n-button>
            </template>
          </NavLeftPrimary>
        </div>
      </template>
    </Header>

    <div class="mobile flex flex-col my-2 mb-8 bg-aic-bg">
      <main class="flex flex-col px-0 grow first-letter:text-left mt-0 mx-1 md:mx-4">
        <router-view v-slot="{ Component }">
          <Transition mode="out-in" :name="route.meta.transition ? String(route.meta.transition) : 'hop'">
            <KeepAlive>
              <Suspense>
                <component :is="Component" class="view main-content" :key="route.path"
                  :class="{ opacity0: route_is_loading }" />
                <template #fallback>
                  <LoadingSpinner />
                </template>
              </Suspense>
            </KeepAlive>
          </Transition>
        </router-view>
      </main>
    </div>
  </template>

  <!-- 
    DESKTOP 
  -->
  <template v-else>
    <Header @clickLogo="router.push({ name: 'home' })" :shadow="y > 20" :admin="isDoctor" class="select-none"
      background="lg:transparent" :hidePageTitle="(y > 100 && width > 1280) || (y > 20 && width <= 1280)">
      <template #right>
        <!-- second button from the right, aligned left -->
        <template v-if="isDoctor">

          <div class="flex flex-row items-start w-64 space-x-3">
            <img class="w-12 rounded-full" src="/dusek.jpeg" alt="Lékař">
            <div class="flex flex-col space-y-1 mt-1.5">
              <span class="font-bold">MUDr. Vítězslav Dušek</span>
              <span>Klinika detské onkologie</span>
            </div>
          </div>
        </template>
      </template>
      <template #right2 v-if="y <= 100">
        <LogoutButton />
      </template>
    </Header>

    <div class="layout-content flex flex-col">
      <nav aria-label="Sidebar" class="select-none">
        <RouterView name="LeftSidebar" @clickedEntry="clickedNavEntry" />
      </nav>

      <div class="flex flex-row ml-16 xl:ml-64 mt-2 mb-8">
        <main class="flex flex-col text-left pl-10 2xl:pl-16 px-8 w-full">
          <template v-if="route_is_loading">
            <Transition mode="out-in" name="fade">
              <LoadingSpinner />
            </Transition>
          </template>
          <template v-else>
            <div class="main-layout-page">
              <div class="flex space-x-2">
                <h1 v-if="parentParentRoute" class="page-link">
                  <RouterLink :to="{ name: parentParentRoute.name as string }">{{ parentParentRoute.meta.headline }}
                  </RouterLink>
                  <n-icon class="ml-2 relative top-1 text-slate-500">
                    <ChevronForward />
                  </n-icon>
                </h1>
                <h1 v-if="route.meta?.parentName" class="page-link">
                  <RouterLink :to="{ name: route.meta.parentName as string }">{{ parentHeadline }}</RouterLink>
                  <n-icon class="ml-2 relative top-1 text-slate-500">
                    <ChevronForward />
                  </n-icon>
                </h1>
                <h1 v-if="!mobile">
                  {{ route.meta?.headline }}
                </h1>
              </div>
              <p v-if="route.meta?.description">
                {{ route.meta?.description }}
              </p>
              <router-view v-slot="{ Component }">
                <component :is="Component" class="view main-content z-10" :key="route.path" ref="currentComponent"
                  :class="{ opacity0: route_is_loading }" />
              </router-view>
            </div>
          </template>
        </main>
      </div>
    </div>
  </template>
</template>

<script setup lang="ts">
import { LogOutOutline, ChevronForward, ChevronBack } from "@vicons/ionicons5";
import { useRouter, useRoute } from "vue-router";
import { useWindowScroll, useWindowSize } from "@vueuse/core";
import { computed, inject, ref } from "vue";
import { useLoadingBar } from "naive-ui";
import { default_route_name } from "@/router";
import { useOptionsStore } from "@/stores/options";

const mobile = inject('mobile');
const router = useRouter();
const route = useRoute();
const route_is_loading = ref(false);
const loadingBar = useLoadingBar();
const { y } = useWindowScroll();
const { width } = useWindowSize();

const options = useOptionsStore();
const isDoctor = computed(() => {
  const routeName = route.name;
  return typeof routeName === 'string' && routeName.startsWith('doctor');
});

const props = defineProps<{
  disableChildComponentTransition?: boolean;
}>();

const currentComponent = ref();
// reset the page (if defined by component) if clicked on the same nav entry
function clickedNavEntry(routeName: string) {
  if (currentComponent?.value && currentComponent.value.reset !== undefined) {
    currentComponent.value.reset();
  }
}

const parentRoute = computed(() => router.getRoutes().find(r => r.name === route.meta?.parentName));
const parentParentRoute = computed(() => {
  const parent = router.getRoutes().find(r => r.name === route?.meta?.parentName && r.meta?.parentName);
  return router.getRoutes().find(r => r.name === parent?.meta?.parentName && r?.meta?.headline);
});
const parentHeadline = ref<string | null>(parentRoute && parentRoute.value?.meta ? parentRoute.value.meta?.headline as string : null);

let loadingTimeout: ReturnType<typeof setTimeout> = setTimeout(() => { }, 0);
router.beforeEach(() => {
  loadingBar.start();
  loadingTimeout = setTimeout(() => (route_is_loading.value = true), 1000);
  parentHeadline.value = parentRoute.value?.meta?.headline as string;
});
router.afterEach(() => {
  clearTimeout(loadingTimeout);
  loadingBar.finish();
  route_is_loading.value = false;
  parentHeadline.value = parentRoute.value?.meta?.headline as string;
});
router.isReady().then(() => {
  clearTimeout(loadingTimeout);
  loadingBar.finish();
  route_is_loading.value = false;
});
</script>

<style scoped>
.hop-enter-active,
.hop-leave-active {
  transition: opacity 0.12s, transform 0.12s;
}

.hop-enter-from,
.hop-leave-to {
  opacity: 0;
  transform: translateX(-0.5%);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.opacity0 {
  opacity: 0;
}

#btn-logout {
  width: 100%;
}
</style>
