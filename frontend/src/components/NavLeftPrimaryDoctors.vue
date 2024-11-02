<template>
  <template v-if="mobile && !open">
    <div class="relative top-0.5">
      <a @click="open = !open">
        <n-icon size="36"><MenuIcon /></n-icon>
      </a>
    </div>
  </template>

  <template v-else-if="mobile && open">
    <div class="relative top-0.5">
      <n-icon size="36"><MenuIcon /></n-icon>
    </div>

    <n-drawer v-model:show="open" width="80%" style="max-width: 22rem;" placement="left">
      <n-drawer-content title="Navigace" closable>
        <div class="flex flex-col space-y-8 items-justify mx-2">
        <n-menu
          :options="menuOptions"
          :icon-size="28"
          @update:value="open = false"
        />
        <div class="text-left mx-2.5"><slot name="menuDrawer"></slot></div>
        </div>
      </n-drawer-content>
    </n-drawer>
    <div class="fixed top-20 left-0 right-0 w-16 h-16">
      <a @click="open = !open">
        <n-icon size="36"><MenuIcon /></n-icon>
      </a>
    </div>
  </template>

  <template v-else>
    <div class="fixed top-20 left-0 right-0 w-[4.6rem] xl:w-full max-w-fit transition-all ease-in-out"
      :class="{ '!w-[4.5rem]': y > 100 }">
      <n-menu :options="menuOptions" v-model:value="selectedKey" :icon-size="28" class="transition-all ease-in-out" />
    </div>
  </template>
</template>

<script setup lang="ts">
// TODO: https://www.naiveui.com/en-US/light/components/menu collapsed sider
import { h, Component, ref, watch } from "vue";
import { NIcon } from "naive-ui";
import type { MenuOption } from "naive-ui";
import { RouterLink } from "vue-router";
import { Menu as MenuIcon } from "@vicons/ionicons5";
import Icon from "./Icon.vue";
import { useRoute } from "vue-router";
import { default_route_name } from "@/router";
import router from "@/router";
import { useWindowScroll } from "@vueuse/core";

const { y } = useWindowScroll();

const props = defineProps<{
  mobile?: boolean;
}>();

const open = ref(false);

function renderIcon(icon: Component, name?: string) {
  return () => h(NIcon, null, { default: () => h(icon, { name }) });
}

const menuOptions: MenuOption[] = [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "doctor-home",
          },
        },
        { default: () => "Pacienti" }
      ),
    key: "doctor-home",
    icon: renderIcon(Icon, "patient"),
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: "doctor-surveys",
          },
        },
        { default: () => "Dotazníky" }
      ),
    key: "doctor-surveys",
    icon: renderIcon(Icon, "survey"),
  }
];

// make sure the selected menu item matches the route
const route = useRoute();
const selectedKey = ref(
  fuzzyMatchOptionKey(route.name?.toString(), menuOptions)
);

function fuzzyMatchOptionKey(
  key: string | undefined,
  options: MenuOption[]
): string {
  if (!key || !key.length) return "doctor-home";
  for (const option of options) {
    if (key.startsWith(String(option.key))) return String(option.key);
  }
  return default_route_name;
}

watch(
  () => route.name,
  async (newName) => {
    selectedKey.value = fuzzyMatchOptionKey(newName?.toString(), menuOptions);
  }
);
</script>

<style>
/** for some reason, cannot move it to index.css */
.n-menu .n-menu-item {
  height: calc(var(--n-item-height) * 1.2);
  /*padding-right: 1rem;*/
  min-width: 16rem;
  .n-menu-item-content {
    padding-right: 1.5rem;
  }
}

.n-menu-item-content {
  height: 3.5rem !important;
}

.n-menu-item-content-header {
  @apply ml-1;
}
</style>
