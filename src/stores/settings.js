import { PROJECT_STORAGE, SETTINGS_REMEMBER_PROJECT } from "@/constants";
import { useStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { ref } from "vue";

export const useSettingsStore = defineStore("settings", () => {
  const isOpen = ref(false);
  const theme = ref("245 158 11");
  const rememberProject = ref(useStorage(SETTINGS_REMEMBER_PROJECT, false));

  const setIsOpen = (state) => {
    isOpen.value = state;
  };
  const setTheme = (theme) => {
    theme.value = theme;
  };
  const setRememberProject = (state) => {
    if (!state) localStorage.removeItem(PROJECT_STORAGE);
    rememberProject.value = state;
  };

  return {
    isOpen,
    setIsOpen,
    theme,
    setTheme,
    rememberProject,
    setRememberProject,
  };
});
