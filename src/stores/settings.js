import axios from "axios";
import { SETTINGS_REMEMBER_PROJECT, SETTINGS_THEME } from "@/constants";
import { useStorage } from "@vueuse/core";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useGlobalStore } from "./global";

export const useSettingsStore = defineStore("settings", () => {
  const isOpen = ref(false);
  const theme = ref(useStorage(SETTINGS_THEME, "245 158 11"));
  const rememberProject = ref(useStorage(SETTINGS_REMEMBER_PROJECT, false));

  const globalStore = useGlobalStore();
  const { setSettingsLoading } = globalStore;

  const setIsOpen = (state) => {
    isOpen.value = state;
  };

  const getSetting = async (name, language) => {
    setSettingsLoading(true);
    let params = {};
    if (language) params["language"] = language;
    const response = await axios
      .get(`/api/settings/${name}`, {
        params: params,
      })
      .catch((error) => {
        if (error.status !== 200) {
          return null;
        }
      });
    if (!response) return;

    const data = await response.data;
    setSettingsLoading(false);
    return data;
  };
  const saveSetting = async (name, content, language) => {
    setSettingsLoading(true);
    const response = await axios
      .put(`/api/settings/${name}`, {
        content: content,
        language: language,
      })
      .catch((error) => {
        if (error.status !== 200) {
          return null;
        }
      });
    if (!response) return;
    const data = await response.data;
    setSettingsLoading(false);
    return data;
  };
  const deleteSetting = async (name, language) => {
    setSettingsLoading(true);
    let params = {};
    if (language) params["language"] = language;
    const response = await axios
      .delete(`/api/settings/${name}`, {
        params: params,
      })
      .catch((error) => {
        if (error.status !== 200) {
          return null;
        }
      });
    if (!response) return;
    const data = await response.data;
    setSettingsLoading(false);
    return data;
  };

  return {
    isOpen,
    setIsOpen,
    theme,
    rememberProject,
    getSetting,
    saveSetting,
  };
});
