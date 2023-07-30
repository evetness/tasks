<script>
export default {
  name: "Label",
  props: ["for", "disabled", "error"],
  data() {
    return {
      id: `${this.for}-input`,
    }
  }
}
</script>

<template>
    <label :for="id" :class="{
      'text-stone-500/80': disabled,
      'text-red-500/80': error,
      'text-brand/80': !disabled && !error
    }" class="font-medium">
        <slot></slot>
    </label>
</template>
