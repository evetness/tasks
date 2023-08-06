<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectCard from "@/components/organisms/ProjectCard.vue";
import WageCard from "@/components/organisms/WageCard.vue";
import TaskCard from '@/components/organisms/TaskCard.vue';

export default {
  name: "App",
  components: { FontAwesomeIcon, ProjectCard, WageCard, TaskCard },
  computed: {
    ...mapState(useProjectStore, {
      selected: "id"
    })
  }
}
</script>

<template>
  <div class="grid grid-cols-4 grid-rows-6 gap-6 w-full p-6 md:h-screen">
    <div class="col-span-1 row-start-1" :class="{'row-span-4': selected, 'row-span-full': !selected}">
      <ProjectCard/>
    </div>

    <div v-if="selected" class="col-span-1 row-start-5 row-span-2">
      <WageCard/>
    </div>

    <div class="col-span-3 row-span-full">
      <TaskCard/>
    </div>
  </div>
</template>