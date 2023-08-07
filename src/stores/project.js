import { defineStore } from 'pinia'

// useLocalStorage from vueuse for storing project id
export const useProjectStore = defineStore('project', {
  state: () => ({ id: 0 }),
  actions: {
    selectProject(id) { this.id = id }
  }
})
