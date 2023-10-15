import {defineStore, storeToRefs} from "pinia";
import {ref} from "vue";

import {useGlobalStore} from "@/stores/global.js";
import {useProjectStore} from "@/stores/project.js";

import axios from "axios";
import {sortByDate} from "@/utils.js";

export const useWageStore = defineStore('wage', () => {
  const globalStore = useGlobalStore();
  const {search} = storeToRefs(globalStore);
  const {setWagesLoading} = globalStore;

  const projectStore = useProjectStore();
  const {selected} = storeToRefs(projectStore)
  const {getCurrentWage, getUnpaidSalary} = projectStore;

  const wages = ref([]);

  const updateWages = (wage) => {
    const index = wages.value.findIndex((obj => obj.id === wage.id));
    if (index >= 0) {
      wages.value[index] = wage;
    } else {
      wages.value.push(wage);
    }
    wages.value.sort((a, b) => sortByDate(a, b, "date"));
    getCurrentWage();
    getUnpaidSalary();
  }
  const removeWage = (id) => {
    wages.value = wages.value.filter((obj => obj.id !== id))
    getCurrentWage();
    getUnpaidSalary();
  }
  const getWages = async (query) => {
    if (!selected.value) {
      wages.value = [];
      return
    }
    setWagesLoading(true);

    const defaultQuery = {page: 1, per_page: 0, order_by: 'date', order: 'desc'};

    const response = await axios.get('/api/wages', {
      params: {...defaultQuery, ...query, project_id: selected.value, search: search.value}
    });
    const data = await response.data;
    wages.value = data.items;

    setWagesLoading(false);
  }


  return {
    wages,
    getWages, updateWages, removeWage
  }
});