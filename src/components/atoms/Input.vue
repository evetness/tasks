<script setup>
import { computed, defineOptions } from 'vue';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

const props = defineProps(['name', 'errors', 'modelValue', 'disabled']);
const emits = defineEmits(['update:modelValue']);

const id = computed(() => `${props.name}-input`);
const invalid = computed(() => !!(props.errors && props.errors.length > 0));
const value = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emits('update:modelValue', value)
  }
})

defineOptions({
  inheritAttrs: false
})
</script>

<template>
  <div :class="{
    'border-brand/10 bg-brand/5': props.disabled,
    'border-brand/80 bg-brand/10': !props.disabled
  }" class="relative flex items-center gap-2 w-full rounded">
    <slot name="prefix"></slot>
    <slot name="input">
      <input :id="id" :name="props.name" type="text" v-bind="$attrs" v-model="value" :class="{
        'caret-brand focus:bg-brand/20 text-brand hover:bg-brand/20 placeholder:text-brand/50 autofill:!bg-brand rounded-r': !props.disabled
      }" class="block w-full p-1.5 bg-transparent border-none tracking-normal" ref="input"
        :disabled="props.disabled" />
    </slot>
    <div v-if="invalid" class="flex absolute inset-y-0 right-0 items-center pr-3 pointer-events-none">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 text-brand/80" shake
        style="--fa-animation-duration: 2s;" />
    </div>
  </div>
</template>
