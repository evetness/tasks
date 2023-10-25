<script>
import { mapState, mapWritableState } from 'pinia'
import moment from "moment/min/moment-with-locales";
import { useSettingsStore } from "@/stores/settings.js";
import { useProjectStore } from '@/stores/project'
import { useGlobalStore } from "@/stores/global.js";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectList from "@/components/organisms/ProjectList.vue";
import WageCard from "@/components/organisms/WageCard.vue";
import TaskList from '@/components/organisms/TaskList.vue';

export default {
  name: "App",
  components: { FontAwesomeIcon, ProjectList, WageCard, TaskList },
  computed: {
    ...mapWritableState(useSettingsStore, ["theme"]),
    ...mapState(useProjectStore, ["selected"]),
    ...mapWritableState(useGlobalStore, ["search", "inAction"]),
  },
  watch: {
    selected() {
      this.inAction = false
    }
  },
  created() {
    const language = navigator.language || (navigator.languages || ["en"])[0]
    moment.locale(language)
    document.documentElement.style.setProperty("--color-brand", this.theme)
  }
}
</script>

<template>
  <main class="p-4 h-screen">
    <div class="container mx-auto">
      <div class="text-2xl font-extrabold text-brand mb-3 flex items-center gap-3 uppercase">
        <font-awesome-icon icon="clipboard-list" />
        Tasks
      </div>
      <ProjectList />
      <TaskList />
    </div>
  </main>
</template>