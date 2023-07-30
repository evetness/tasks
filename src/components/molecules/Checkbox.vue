<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Label from "@/components/atoms/Label.vue";

export default {
  name: "Input",
  inheritAttrs: false,
  props: ['name', 'type', 'label', 'invalid', 'errors', 'modelValue'],
  components: { FontAwesomeIcon, Label },
  emits: ["update:modelValue"],
  data() {
    return {
      id: `${this.name}-input`
    }
  },
  computed: {
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit('update:modelValue', value)
      }
    }
  }
}
</script>

<template>
  <div :class="{
    'border-red-500/80 bg-red-500/10': invalid,
    'border-brand/80 bg-brand/10': !invalid
  }" class="relative flex items-center gap-2 text-sm border-x group">
    <slot name="input">
      <input :id="id" :name="name" type="checkbox" v-bind="$attrs" v-model="value" class="w-0 h-0 peer" />
      <label :for="id" :class="{
        'border-red-500/80 peer-checked:before:bg-red-500/80 group-hover:bg-red-500/30 peer-focus:bg-red-500/30': invalid,
        'border-brand/80 peer-checked:before:bg-brand/70 group-hover:bg-brand/30 peer-focus:bg-brand/30': !invalid
      }"
        class="inline-flex items-center justify-center h-4 w-4 border before:block before:h-2 before:w-2">
      </label>
    </slot>
    <slot name="label">
      <Label :for="name" :error="invalid" :disabled="false" class="leading-none my-2 flex-auto">
        {{ label }}
      </Label>
    </slot>
    <div v-if="invalid" class="flex absolute inset-y-0 right-0 items-center pr-3 pointer-events-none">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 text-red-600"></font-awesome-icon>
    </div>
  </div>
</template>
