<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectCard from "@/components/organisms/ProjectCard.vue";
import WageCard from "@/components/organisms/WageCard.vue";
import TaskCard from '@/components/organisms/TaskCard.vue';
import moment from "moment/min/moment-with-locales";

export default {
  name: "App",
  components: { FontAwesomeIcon, ProjectCard, WageCard, TaskCard },
  data() {
    return {
      page: "tasks"
    }
  },
  computed: {
    ...mapState(useProjectStore, { selected: "id" })
  },
  created() {
    const language = navigator.language || (navigator.languages || ["en"])[0]
    moment.locale(language)
  }
}
</script>

<template>
  <div class="grid grid-cols-4 gap-6 w-full p-6 md:h-screen">
    <div class="col-span-1">
      <ProjectCard/>
    </div>

    <div class="col-span-3">
      <div class="h-full flex flex-col card">
        <ul class="flex flex-wrap text-sm font-medium text-center border-b border-brand/60 space-x-1 -mt-3 -mx-3 mb-3">
          <li>
            <button type="button" class="inline-block p-4 uppercase" :class="{
              'text-brand/80 bg-brand/20': this.page === 'tasks',
              'text-brand/80 hover:bg-brand/10': this.page !== 'tasks'
            }" @click="this.page = 'tasks'">
              Tasks
            </button>
          </li>
          <li>
            <button type="button" class="inline-block p-4 uppercase" :class="{
              'text-brand/80 bg-brand/20': this.page === 'wages',
              'text-brand/80 hover:bg-brand/10': this.page !== 'wages'
            }" @click="this.page = 'wages'">
              Wages
            </button>
          </li>
        </ul>
        <WageCard v-if="this.page === 'wages'"/>
        <TaskCard v-if="this.page === 'tasks'"/>
      </div>
    </div>
  </div>
</template>