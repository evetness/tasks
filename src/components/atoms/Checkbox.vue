<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Label from "@/components/atoms/Label.vue";

export default {
  name: "Input",
  inheritAttrs: false,
  props: ["name", "type", "label", "errors", "modelValue"],
  components: { FontAwesomeIcon, Label },
  emits: ["update:modelValue"],
  data() {
    return {
      id: `${this.name}-input`
    }
  },
  computed: {
    invalid() { return this.errors && this.errors.length > 0 ? true : false },
    value: {
      get() {
        return this.modelValue
      },
      set(value) {
        this.$emit("update:modelValue", value)
      }
    }
  }
}
</script>

<template>
  <div :class="{'border-dashed': invalid }" 
       class="relative flex items-center gap-2 text-sm border-brand/80 bg-brand/10 border-x group">
    <slot name="input">
      <input :id="id" :name="name" type="checkbox" v-bind="$attrs" v-model="value" class="w-0 h-0 peer" />
      <label :for="id"
        class="inline-flex items-center justify-center h-4 w-4 border before:block before:h-2 before:w-2 border-brand/80 peer-checked:before:bg-brand/70 group-hover:bg-brand/30 peer-focus:bg-brand/30">
      </label>
    </slot>
    <slot name="label">
      <Label :for="name" :disabled="false" class="leading-none my-2 flex-auto">
        {{ label }}
      </Label>
    </slot>
    <div v-if="invalid" class="flex absolute inset-y-0 right-0 items-center pr-3 pointer-events-none">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 text-brand/80"></font-awesome-icon>
    </div>
  </div>
</template>
