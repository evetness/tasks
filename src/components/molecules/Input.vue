<script>
import {FontAwesomeIcon} from "@fortawesome/vue-fontawesome";
import Label from "@/components/atoms/Label.vue";

export default {
  name: "Input",
  inheritAttrs: false,
  props: ['name', 'type', 'label', 'invalid', 'errors', 'modelValue'],
  components: {FontAwesomeIcon, Label},
  emits: ["update:modelValue"],
  data() {
    return {
      id: `${this.name}-input`
    }
  },
  mounted() {
    this.$refs.input.focus()
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
        'border-red-500/80 bg-red-500/10 border-x-4': invalid, 
        'border-brand/80 bg-brand/10 border-x': !invalid
    }" class="relative flex items-center gap-2 text-sm w-full">
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
            <input :id="id" :name="name" :type="type || 'text'" v-bind="$attrs" v-model="value" :class="{
                'caret-red-500 focus:bg-red-500/30 text-red-500 hover:bg-red-500/30 placeholder:text-red-500/50': invalid,
                'caret-brand focus:bg-brand/30 text-brand hover:bg-brand/30 placeholder:text-brand/50 autofill:!bg-brand': !invalid
            }" class="block w-full p-1.5 bg-transparent border-none text-sm tracking-normal" ref="input"/>
        </slot>
        <div v-if="invalid" class="flex absolute inset-y-0 right-0 items-center pr-3 pointer-events-none">
            <font-awesome-icon icon="triangle-exclamation" class="w-4 h-4 text-red-500" shake style="--fa-animation-duration: 2s;"></font-awesome-icon>
        </div>
    </div>
</template>
