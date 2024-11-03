<template>
  <a class="flex flex-col justify-between aic-window window-hover shadow-lg h-full" @click="emit('clickContent')">
    <div class="flex-shrink-0 p-0.5">
      <img class="h-32 w-full object-cover object-top rounded-lg rounded-b-none border-b-2 opacity-50" :src="previewUrl"
        alt="" v-if="previewUrl" />
    </div>
    <div class="flex-1 p-6 flex flex-col justify-between">
      <div class="flex-1">
        <n-icon size="24">
          <BookOutline />
        </n-icon>
        <p class="text-base font-medium text-aic-primary">
          <!-- TODO: links to filter class="hover:underline" -->
          <span v-for="(topic, idx) of d.topics">
            {{ topic }}{{ d.topics.length > 1 && idx < d.topics.length - 1 ? ', ' : '' }} </span>
        </p>
        <a class="block mt-2">
          <p class="text-lg font-semibold text-gray-900">
            {{ d.title }}
          </p>
          <p class="mt-3 text-base text-gray-500" v-if="d?.description">
            {{ d.description }}
          </p>
        </a>
      </div>
      <div v-if="d?.author" class="mt-6 flex items-center">
        <div class="flex-shrink-0">
          <a v-if="d?.author" :href="d.author.href" noopener norefferer>
            <span class="sr-only">{{ d.author.name }}</span>
            <img class="h-10 w-10 rounded-full" :src="d.author.imageUrl" alt="" />
          </a>
        </div>
        <div class="ml-3">
          <p class="text-sm font-medium text-gray-900">
            <a v-if="d?.author" :href="d.author.href" noopener norefferer class="hover:underline">
              {{ d?.author.name }}
            </a>
          </p>
          <div v-if="d?.readingTime" class="flex space-x-1 text-sm text-gray-500">
            <time v-if="d?.datetime" :datetime="d.datetime">
              {{ d?.date }}
            </time>
            <span aria-hidden="true"> &middot; </span>
            <span> {{ d?.readingTime }} čtení </span>
          </div>
        </div>
      </div>
    </div>
  </a>
</template>

<script setup lang="ts">
import { BookOutline } from "@vicons/ionicons5"
import { computed } from "vue";

const props = defineProps<{
  d: any;
}>();

const previewUrl = computed(() => {
  return "/edu-example/1/Brožurka20FN20Brno202-1.jpg";//"+props.d.fileId+".jpg";
});

const titleSlug = computed(() => {
  return props.d.title.toLocaleLowerCase().replace(' ', '-');
});

const emit = defineEmits<{
  clickContent: [];
}>();
</script>

<style scoped>
a {
  @apply cursor-pointer;
}

p {
  @apply mb-0;
}
</style>