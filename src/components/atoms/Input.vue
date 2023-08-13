<script>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import Label from "@/components/atoms/Label.vue";

export default {
  name: "Input",
  inheritAttrs: false,
  props: ["name", "type", "label", "errors", "modelValue", "autofocus"],
  components: { FontAwesomeIcon, Label },
  emits: ["update:modelValue"],
  data() {
    return {
      id: `${this.name}-input`
    }
  },
  mounted() {
    if (this.autofocus) {
      this.$refs.input.focus()
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
  },
  updated() {
    console.log(this.errors)
  }
}
</script>

<template>
  <div :class="{
    'border-dashed border-x-4': invalid,
    'border-x': !invalid
  }" class="relative flex items-center gap-2 text-sm w-full border-brand/80 bg-brand/10">
    <slot name="label">
      <Label :for="name" :error="invalid" :disabled="false" :class="{
        'font-bold': invalid,
        'ml-2': label,
        'hidden': !label
      }">
        {{ label }}
      </Label>
    </slot>
    <slot name="input">
      <input :id="id" :name="name" :type="type || 'text'" v-bind="$attrs" v-model="value"
             class="block w-full p-1.5 bg-transparent border-none text-sm tracking-normal caret-brand focus:bg-brand/20 text-brand hover:bg-brand/20 placeholder:text-brand/50 autofill:!bg-brand" ref="input" />
    </slot>
    <div v-if="invalid" class="flex absolute inset-y-0 right-0 items-center pr-3 pointer-events-none">
      <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 text-brand/80" shake
        style="--fa-animation-duration: 2s;"></font-awesome-icon>
    </div>
  </div>
</template>
