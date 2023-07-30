<script>
export default {
  name: "ProjectItem"
}
</script>

<template>
  <div class="flex items-center hover:bg-brand/20 focus:bg-brand/20 border-x" :class="{
      'border-transparent': !selected || selected != project.id,
      'border-brand/60 bg-brand/10': selected && selected == project.id
    }">
    <button class="w-full py-2 px-3 text-left text-brand" @click="this.selectProject(project.id)">
      {{ project.name }}
    </button>
    <button class="btn hover:bg-brand/20">
      <font-awesome-icon icon="fa-regular fa-pen-to-square" />
    </button>
    <button class="btn hover:bg-brand/20">
      <font-awesome-icon icon="fa-regular fa-trash-can" />
    </button>
  </div>
</template>