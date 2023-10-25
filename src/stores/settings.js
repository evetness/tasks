import { defineStore } from 'pinia';


export const useSettingsStore = defineStore('settings', {
  state: () => ({ theme: '245 158 11' }),
  actions: {
    setTheme(theme) {
      this.theme = theme;
    }
  }
})