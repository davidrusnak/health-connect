import { defineStore } from "pinia";
import { ref } from "vue";

export const useOptionsStore = defineStore("options", () => {
  const userRole = ref("doctor");

  return { userRole };
});
