<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'

export default {
  name: "ProjectItem",
  props: ["id", "name"],
  computed: {
    ...mapState(useProjectStore, {
      selected: "id"
    })
  },
  methods: {
    ...mapActions(useProjectStore, ["selectProject"])
  },
  emits: ["project:edit", "project:remove"],
}
</script>

<template>
  <div class="flex items-center text-brand/80 text-sm group hover:bg-brand/20 focus-within:bg-brand/20 border-x" :class="{
      'border-transparent': !selected || selected != id,
      'border-brand/60 bg-brand/10': selected && selected == id
    }">
    <button type="button" class="w-full py-2 px-3 text-left text-brand" @click="this.selectProject(this.id)">
      {{ name }}
    </button>

    <button type="button" class="btn btn-text" @click="$emit('project:edit', this.id)">
      <font-awesome-icon icon="fa-regular fa-pen-to-square" />
    </button>
    
    <button type="button" class="btn btn-text" @click="$emit('project:remove', this.id)">
      <font-awesome-icon icon="fa-regular fa-trash-can" />
    </button>
  </div>
</template>