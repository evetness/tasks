import { defineStore } from "pinia";
import { ref } from "vue";

export const useToastStore = defineStore("toast", () => {
  const toasts = ref([]);

  const addToast = (icon, message, dismissable = true, timeout = 5000) => {
    const toast = { icon, message, dismissable, timeout };
    toasts.value.push(toast);
    const index = toasts.value.indexOf(toast);

    if (timeout !== 0) {
      setTimeout(() => {
        removeToast(index);
      }, timeout);
    }
    return index;
  };
  const removeToast = (index) => {
    toasts.value.splice(index, 1);
  };

  return {
    toasts,
    addToast,
    removeToast,
  };
});
