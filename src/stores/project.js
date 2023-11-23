import axios from "axios";
import { defineStore, storeToRefs } from "pinia";
import { useStorage } from "@vueuse/core";

import { formatCurrency, sortByString } from "@/utils";
import { computed, ref } from "vue";
import { useGlobalStore } from "@/stores/global.js";
import { useSettingsStore } from "@/stores/settings.js";
import { PROJECT_STORAGE, SETTINGS_REMEMBER_PROJECT } from "@/constants";

// useLocalStorage from vueuse for storing project id
export const useProjectStore = defineStore("project", () => {
  const globalStore = useGlobalStore();
  const { setProjectLoading, setCurrentWageLoading, setSalaryLoading } =
    globalStore;

  const settingStore = useSettingsStore();
  const { rememberProject } = storeToRefs(settingStore);

  const _selected = ref(0);
  const projects = ref([]);
  const wage = ref(null);
  const salary = ref(null);

  const selected = computed({
    get() {
      if (rememberProject.value) {
        const state = useStorage(PROJECT_STORAGE, 0);
        return state.value;
      }
      return _selected.value;
    },
    set(value) {
      if (rememberProject.value) {
        const state = useStorage(PROJECT_STORAGE, 0);
        state.value = value;
      }
      _selected.value = value;
    },
  });
  const amount = computed(() => {
    return wage.value
      ? formatCurrency(wage.value.amount, wage.value.currency)
      : "-";
  });
  const unpaid = computed(() => {
    return salary.value
      ? formatCurrency(salary.value.amount, salary.value.currency)
      : "-";
  });
  const elapsed = computed(() => {
    return salary.value ? salary.value.elapsed : "00:00";
  });
  const project = computed(() => {
    return projects.value.find((obj) => obj.id === selected.value);
  });

  const selectProject = async (id) => {
    if (id === selected.value) return null;
    selected.value = id;
    getCurrentWage();
    getUnpaidSalary();
  };
  const getProjects = async (query) => {
    setProjectLoading(true);

    const defaultQuery = {
      page: 1,
      per_page: 0,
      order_by: "name",
      order: "asc",
    };

    const response = await axios.get("/api/projects", {
      params: { ...defaultQuery, ...query },
    });
    const data = await response.data;
    projects.value = data.items;

    setProjectLoading(false);
  };
  const updateProjects = (project) => {
    const index = projects.value.findIndex((obj) => obj.id === project.id);
    if (index >= 0) {
      projects.value[index] = project;
    } else {
      projects.value.push(project);
    }
    projects.value.sort((a, b) => sortByString(a, b, "name"));
    selectProject(project.id);
  };
  const removeProject = (id) => {
    if (selected.value === id) {
      selectProject(0);
    }
    projects.value = projects.value.filter((obj) => obj.id !== id);
  };
  const getCurrentWage = async () => {
    setCurrentWageLoading(true);
    const response = await axios.get(`/api/projects/${selected.value}/wage`);
    const data = await response.data;
    if (Object.keys(data).length === 0) {
      wage.value = null;
    } else {
      wage.value = data;
    }
    setCurrentWageLoading(false);
  };
  const getUnpaidSalary = async () => {
    setSalaryLoading(true);
    const response = await axios.get(`/api/projects/${selected.value}/salary`);
    const data = await response.data;
    if (Object.keys(data).length === 0) {
      salary.value = null;
    } else {
      salary.value = data;
    }
    setSalaryLoading(false);
  };

  return {
    selected,
    projects,
    project,
    wage,
    salary,
    amount,
    unpaid,
    elapsed,
    selectProject,
    getProjects,
    updateProjects,
    removeProject,
    getCurrentWage,
    getUnpaidSalary,
  };
});
