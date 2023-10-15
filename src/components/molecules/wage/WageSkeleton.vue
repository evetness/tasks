<script>
export default {
  name: "WageSkeleton",
  computed: {
    size() {
      return Math.floor(Math.random() * 10) + 1
    }
  }
}
</script>

<template>
  <div v-for="n in size" class="w-full animate-pulse bg-brand/20 h-9"></div>
</template>