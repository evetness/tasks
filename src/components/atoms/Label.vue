<script setup>
import { computed } from 'vue';
const props = defineProps(['for', 'disabled']);

const id = computed(() => `${props.for}-input`)
</script>

<template>
  <label :for="id" :class="{
    'text-stone-500/80': disabled,
    'text-brand/80': !disabled
  }" class="font-medium">
      <slot></slot>
  </label>
</template>
