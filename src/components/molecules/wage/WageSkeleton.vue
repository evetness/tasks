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
  <tr v-for="n in size" class="group animate-pulse bg-brand/20 h-9">
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</template>