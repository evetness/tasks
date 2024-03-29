import { defineStore } from "pinia";
import { ref } from "vue";

export const useGlobalStore = defineStore("global", () => {
  const inAction = ref(false);
  const isProjectLoading = ref(false);
  const isCurrentWageLoading = ref(false);
  const isSalaryLoading = ref(false);
  const isTasksLoading = ref(false);
  const isWagesLoading = ref(false);
  const isSettingsLoading = ref(false);

  const setAction = (state) => {
    inAction.value = state;
  };
  const setProjectLoading = (state) => {
    isProjectLoading.value = state;
  };
  const setCurrentWageLoading = (state) => {
    isCurrentWageLoading.value = state;
  };
  const setSalaryLoading = (state) => {
    isSalaryLoading.value = state;
  };
  const setTasksLoading = (state) => {
    isTasksLoading.value = state;
  };
  const setWagesLoading = (state) => {
    isWagesLoading.value = state;
  };
  const setSettingsLoading = (state) => {
    isSettingsLoading.value = state;
  }

  return {
    inAction,
    setAction,
    isProjectLoading,
    setProjectLoading,
    isCurrentWageLoading,
    setCurrentWageLoading,
    isSalaryLoading,
    setSalaryLoading,
    isTasksLoading,
    setTasksLoading,
    isWagesLoading,
    setWagesLoading,
    isSettingsLoading,
    setSettingsLoading
  };
});
