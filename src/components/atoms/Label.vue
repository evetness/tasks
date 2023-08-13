<script>
export default {
  name: "Label",
  props: ["for", "disabled"],
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
      'text-brand/80': !disabled
    }" class="font-medium">
        <slot></slot>
    </label>
</template>
