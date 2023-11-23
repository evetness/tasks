import { SETTINGS_REMEMBER_PROJECT, SETTINGS_THEME, TASK_INCOMPLETE, TASK_STATUS_FILTER } from "@/constants";
import { useStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  const isOpen = ref(false);
  const theme = ref(useStorage(SETTINGS_THEME, "245 158 11"));
  const rememberProject = ref(useStorage(SETTINGS_REMEMBER_PROJECT, false));
  const defaultProject = ref(useStorage(TASK_STATUS_FILTER, TASK_INCOMPLETE));

  const setIsOpen = (state) => {
    isOpen.value = state;
  };

  return {
    isOpen,
    setIsOpen,
    theme,
    rememberProject,
    defaultProject
  };
});
