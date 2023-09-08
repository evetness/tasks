<script>
export default {
  name: 'ProjectSkeleton',
  computed: {
    size() {
      return Math.floor(Math.random() * 10) + 1
    }
  }
}
</script>

<template>
  <div class="space-y-1 overflow-y-scroll">
    <div v-for="n in size" class="group animate-pulse">
      <div class="flex items-center gap-0.5 border-x border-transparent">
        <div class="w-full py-2 px-3 text-left bg-brand/20 h-9"></div>
        <div class="btn bg-brand/10 h-9 w-16"></div>
        <div class="btn bg-brand/10 h-9 w-16"></div>
      </div>
    </div>
    <div class="animate-pulse">
      <div class="flex items-center gap-0.5 border-x border-transparent">
        <div class="btn bg-brand/10 h-9 w-full"></div>
      </div>
    </div>
  </div>
</template>