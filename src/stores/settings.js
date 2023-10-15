import { defineStore } from 'pinia';


export const useSettingsStore = defineStore('settings', {
  state: () => ({ theme: '50 141 168' }),
  actions: {
    setTheme(theme) {
      this.theme = theme;
    }
  }
})