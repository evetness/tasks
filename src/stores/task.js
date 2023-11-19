import { defineStore, storeToRefs } from "pinia";
import axios from "axios";
import { sortByDate } from "@/utils.js";
import { ref } from "vue";
import { useProjectStore } from "@/stores/project.js";
import { useGlobalStore } from "@/stores/global.js";

export const useTaskStore = defineStore("task", () => {
  const globalStore = useGlobalStore();
  const { setTasksLoading } = globalStore;

  const projectStore = useProjectStore();
  const { selected } = storeToRefs(projectStore);
  const { getUnpaidSalary } = projectStore;

  const tasks = ref([]);
  const search = ref("");
  const status = ref("INCOMPLETE");

  const updateTasks = (task) => {
    const index = tasks.value.findIndex((obj) => obj.id === task.id);
    if (index >= 0) {
      tasks.value[index] = task;
    } else {
      tasks.value.push(task);
    }
    tasks.value.sort((a, b) => sortByDate(a, b, "start"));
    getUnpaidSalary();
  };
  const removeTask = (id) => {
    tasks.value = tasks.value.filter((obj) => obj.id !== id);
    getUnpaidSalary();
  };
  const changeTaskStatus = async (id) => {
    const response = await axios
      .put(`/api/tasks/change-status/${id}`)
      .catch((error) => {
        if (error.response.status === 404) {
          const message = error.response.data.message;
          console.error(message);
        }
        return null;
      });
    if (!response) return;

    const data = response.data;
    updateTasks(data);
  };
  const getTasks = async (query) => {
    if (!selected.value) {
      tasks.value = [];
      return;
    }
    setTasksLoading(true);

    const defaultQuery = {
      page: 1,
      per_page: 0,
      order_by: "start",
      order: "desc",
    };

    const response = await axios.get("/api/tasks", {
      params: {
        ...defaultQuery,
        ...query,
        project_id: selected.value,
        search: search.value,
        status: status.value,
      },
    });
    const data = await response.data;
    tasks.value = data.items;

    setTasksLoading(false);
  };

  return {
    tasks,
    search,
    status,
    getTasks,
    changeTaskStatus,
    updateTasks,
    removeTask,
  };
});
