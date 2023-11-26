<script setup>
import { storeToRefs } from 'pinia';
import { useToastStore } from '@/stores/toast';

import { FontAwesomeIcon, FontAwesomeLayers } from '@fortawesome/vue-fontawesome';

const toastStore = useToastStore();
const { toasts } = storeToRefs(toastStore);
const { removeToast } = toastStore;
</script>

<template>
  <div v-if="toasts.length"
    class="fixed bottom-4 inset-x-0 flex flex-col items-center md:items-end gap-4 sm:right-6 z-50">
    <div v-for="(toast, index) in toasts" :key="index" class="px-2 py-2 bg-stone-900 rounded-xl shadow-xl max-w-sm">

      <div class="flex gap-2">
        <font-awesome-layers class="text-3xl shrink-0">
          <font-awesome-icon icon="square" class="text-brand/10 rounded-xl" />
          <font-awesome-icon :icon="toast.icon" class="text-brand/70" transform="shrink-10" />
        </font-awesome-layers>

        <p class="self-center font-semibold text-sm text-brand/90">{{ toast.message }}</p>

        <button v-if="toast.dismissable" @click="removeToast(index)" class="btn text-xs btn-text ml-auto !px-3 !py-2">
          <font-awesome-icon icon="xmark" />
        </button>
      </div>

    </div>
  </div>
</template>