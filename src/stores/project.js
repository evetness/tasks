import { defineStore } from 'pinia'

export const useProjectStore = defineStore('project', {
  state: () => ({ id: 0 }),
  actions: {
    selectProject(id) { this.id = id }
  }
})
