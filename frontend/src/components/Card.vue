<template>
  <div class="w-full min-w-full h-fit relative flex-col"
  :class="{'bg-white overflow-y-auto sm:rounded-lg aic-window': !disableCardStyle, '!h-full max-h-[87vh]': viewportHeight, '!overflow-y-hidden': hideYScrollbar || loading}">
    <div v-if="loading" class="bg-slate-100 absolute left-0 top-0 w-full h-full transition-all duration-1000" :class="{'opacity-0': !loading, 'opacity-100': loading}">
      <n-spin class="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2" />
    </div>
    <div v-if="!hideHeader && $slots.header" :class="{'px-4 pt-5 sm:px-6': !disableCardStyle && !mobile, 'px-2 pt-3 sm:px-4': mobile && !disableCardStyle}">
      <slot name="header">Title</slot>
    </div>
    <div :class="{'px-4 py-5 sm:px-6 pt-0': !disableCardStyle && !mobile, 'px-2 pt-1 pb-4': !disableCardStyle && mobile, 'h-full overflow-y-auto': viewportHeight, 'max-h-16 truncate': truncateBody, 'pt-3.5': hideHeader, 'mb-2': mobile }">
      <slot></slot>
    </div>
    <template v-if="truncateBody">
    </template>
    <div v-if="!hideFooter" class="flex items-center justify-center px-4 py-3 sm:px-6">
      <slot name="footer"></slot>
    </div>
    <template v-if="cornerPointer">
      <IconCornerPointer />
    </template>
  </div>
</template>

<script setup lang="ts">
import { inject } from 'vue';

const mobile = inject('mobile');

interface Props {
  disableCardStyle?: boolean;
  cornerPointer?: boolean;
  truncateBody?: boolean;
  hideHeader?: boolean;
  hideFooter?: boolean;
  hideYScrollbar?: boolean;
  viewportHeight?: boolean;
  loading?: boolean;
};

const props = withDefaults(defineProps<Props>(), {
  disableCardStyle: false,
  cornerPointer: false,
  truncateBody: false,
  hideHeader: false,
  hideFooter: false,
  hideYScrollbar: false,
  viewportHeight: false,
  loading: false
})
</script>
