<script setup>
import { computed } from 'vue';
import { Switch, SwitchGroup, SwitchLabel } from '@headlessui/vue'

const props = defineProps(['modelValue']);
const emits = defineEmits(['update:modelValue']);

const value = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emits('update:modelValue', value)
  }
})
</script>

<template>
  <SwitchGroup as="div" class="flex items-center justify-between">
    <SwitchLabel class="mr-4 text-brand/80">
      <slot></slot>
    </SwitchLabel>
    <Switch v-model="value" :class='value ? "bg-brand/30" : "bg-stone-600/30"'
      class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-brand/80 focus:ring-offset-2">
      <span :class='value ? "translate-x-6 bg-brand" : "translate-x-1 bg-stone-600"'
        class="inline-block h-4 w-4 transform rounded-full transition-transform" />
    </Switch>
  </SwitchGroup>
</template>