<template>
  <template v-if="mobile && !open">
    <div class="relative top-0.5">
      <a @click="open = !open">
        <n-icon size="36">
          <MenuIcon />
        </n-icon>
      </a>
    </div>
  </template>

  <template v-else-if="mobile && open">
    <div class="relative top-0.5">
      <n-icon size="36">
        <MenuIcon />
      </n-icon>
    </div>

    <n-drawer v-model:show="open" width="80%" style="max-width: 22rem;" placement="left" class="nav-drawer">
      <n-drawer-content title="Navigace" closable>
        <div class="flex flex-col space-y-8 items-justify mx-2">
          <n-menu :options="menuOptions" :icon-size="28" @update:value="open = false" />
          <div class="text-left mx-2.5">
            <slot name="menuDrawer"></slot>
          </div>
        </div>
      </n-drawer-content>
    </n-drawer>
    <div class="fixed top-20 left-0 right-0 w-16 h-16">
      <a @click="open = !open">
        <n-icon size="36">
          <MenuIcon />
        </n-icon>
      </a>
    </div>
  </template>

  <template v-else>
    <div class="fixed top-24 left-0 right-0 w-[4.6rem] xl:w-full max-w-fit transition-all ease-in-out">
      <n-menu :options="menuOptions" v-model:value="selectedKey" :icon-size="28" class="transition-all ease-in-out"
        @update-value="(routeName: string) => emit('clickedEntry', routeName)" />
    </div>
  </template>
</template>

<script setup lang="ts">
import { computed, h, ref, watch } from "vue";
import type { Component } from "vue";
import { NIcon } from "naive-ui";
import type { MenuOption } from "naive-ui";
import { RouterLink } from "vue-router";
import { Menu as MenuIcon } from "@vicons/ionicons5";
import Icon from "./Icon.vue";
import { useRoute } from "vue-router";
import { default_route_name } from "../router";
import { useOptionsStore } from "@/stores/options";

const props = defineProps<{
  mobile?: boolean;
}>();

const open = ref(true);
const route = useRoute();

function renderIcon(icon: Component, name?: string) {
  return () => h(NIcon, null, { default: () => h(icon, { name }) });
}

const emit = defineEmits<{
  clickedEntry: [name: string];
}>();

let menuOptions: MenuOption[] = [];
if (route.name?.toString().startsWith("doctor")) {
  menuOptions = [
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "doctor-home",
            },
          },
          { default: () => "Dashboard" }
        ),
      key: "home",
      icon: renderIcon(Icon, "home"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "doctor-patients",
            },
          },
          { default: () => "Pacienti" }
        ),
      key: "doctor-patients",
      icon: renderIcon(Icon, "home"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "doctor-requests",
            },
          },
          { default: () => "Žádosti" }
        ),
      key: "doctor-requests",
      icon: renderIcon(Icon, "home"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "doctor-edu-resources",
            },
          },
          { default: () => "Edukační materiály" }
        ),
      key: "doctor-edu-resources",
      icon: renderIcon(Icon, "book"),
    }
  ];
} else {
  // patient routes
  menuOptions = [
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "patient-home",
            },
          },
          { default: () => "Domov" }
        ),
      key: "patient-home",
      icon: renderIcon(Icon, "home"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "patient-reports",
            },
          },
          { default: () => "Lékařské zprávy" }
        ),
      key: "patient-reports",
      icon: renderIcon(Icon, "records"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "patient-requests",
            },
          },
          { default: () => "Žádosti" }
        ),
      key: "patient-requests",
      icon: renderIcon(Icon, "ask"),
    },
    {
      label: () =>
        h(
          RouterLink,
          {
            to: {
              name: "patient-edu-resources",
            },
          },
          { default: () => "Edukační materiály" }
        ),
      key: "patient-edu-resources",
      icon: renderIcon(Icon, "book"),
    }
  ];
}




// make sure the selected menu item matches the route
const selectedKey = ref(
  fuzzyMatchOptionKey(route.name?.toString(), menuOptions)
);

function fuzzyMatchOptionKey(
  key: string | undefined,
  options: MenuOption[]
): string {
  if (!key || !key.length) return "home";
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

.nav-drawer .n-drawer-header {
  @apply !mx-4 ml-8;
}
</style>
