<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from '@headlessui/vue'
import Switch from '@/components/atoms/Switch.vue';

import { storeToRefs } from 'pinia';
import { useSettingsStore } from '@/stores/settings';
import { ref, computed, watch } from 'vue';

const settingsStore = useSettingsStore();
const { isOpen, theme, rememberProject } = storeToRefs(settingsStore);
const { setIsOpen } = settingsStore;

const hexToRgb = (hex) => {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
};
const rgbToHex = (r, g, b) => {
  const rgb = (r << 16) | (g << 8) | (b << 0);
  return '#' + (0x1000000 + rgb).toString(16).slice(1);
};

const themeToHex = computed(() => {
  const rgb = theme.value.split(" ");
  return rgbToHex(rgb[0], rgb[1], rgb[2])
});
const colorPicker = ref(themeToHex.value);

watch(colorPicker, (newValue) => {
  const rgb = hexToRgb(newValue);
  theme.value = `${rgb.r} ${rgb.g} ${rgb.b}`;
});
</script>

<template>
  <TransitionRoot appear :show="isOpen" as="template">
    <Dialog as="div" @close="setIsOpen" class="relative z-10">

      <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0" enter-to="opacity-100"
        leave="duration-200 ease-in" leave-from="opacity-100" leave-to="opacity-0">
        <div class="fixed inset-0 bg-stone-950/20" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild as="template" enter="duration-300 ease-out" enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100" leave="duration-200 ease-in" leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95">

            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-stone-900 p-6 text-left align-middle shadow-xl transition-all">

              <DialogTitle as="h3" class="text-lg font-medium leading-6 text-brand/80 flex items-center justify-between">
                Settings
                <button class="btn btn-text" @click="setIsOpen(false)">
                  <font-awesome-icon icon="xmark" />
                </button>
              </DialogTitle>

              <div class="space-y-3 my-5">
                <Switch v-model="rememberProject">
                  Remember Project
                  <div class="text-xs text-brand/50">The application will remember the latest selectect project.</div>
                </Switch>

                <div class="flex items-center justify-between">
                  <label for="theme-color-picker" class="mr-4 text-brand/80">
                    Theme Color
                    <div class="text-xs text-brand/50">The application will use the selected color.</div>
                  </label>
                  <div class="rounded overflow-hidden w-10 h-6">
                    <input id="theme-color-picker" v-model="colorPicker" type="color" />
                  </div>
                </div>
              </div>

              <div class="mt-6">
                <button type="button" class="btn btn-brand" @click="setIsOpen(false)">
                  Close
                </button>
              </div>
            </DialogPanel>

          </TransitionChild>
        </div>
      </div>

    </Dialog>
  </TransitionRoot>
</template>
