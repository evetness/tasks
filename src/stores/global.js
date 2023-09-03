import { defineStore } from 'pinia'


export const useGlobalStore = defineStore('global', {
  state: () => ({ inAction: false }),
  actions: {
    toggleAction(action) { this.inAction = action }
  }
})
