<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogPanel,
  DialogTitle,
} from '@headlessui/vue'

import { storeToRefs } from 'pinia';
import { useSettingsStore } from '@/stores/settings';
import Switch from '@/components/atoms/Switch.vue';

const settingsStore = useSettingsStore();
const { isOpen, rememberProject } = storeToRefs(settingsStore);
const { setIsOpen, setRememberProject } = settingsStore;

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

              <div class="space-y-1 my-3">
                <Switch label="Remember Project" v-model="rememberProject" />
              </div>

              <div class="mt-4">
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
