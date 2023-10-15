<script>
import {mapState, mapWritableState} from 'pinia'
import { useProjectStore } from '@/stores/project'

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectCard from "@/components/organisms/ProjectCard.vue";
import WageCard from "@/components/organisms/WageCard.vue";
import TaskCard from '@/components/organisms/TaskCard.vue';
import moment from "moment/min/moment-with-locales";
import Input from "@/components/atoms/Input.vue";
import {useGlobalStore} from "@/stores/global.js";
import {useSettingsStore} from "@/stores/settings.js";

export default {
  name: "App",
  components: { FontAwesomeIcon, ProjectCard, WageCard, TaskCard, Input },
  data() {
    return {
      page: "tasks"
    }
  },
  computed: {
    ...mapState(useProjectStore, ["selected"]),
    ...mapWritableState(useGlobalStore, ["search", "inAction"]),
    ...mapWritableState(useSettingsStore, ["theme"])
  },
  created() {
    const language = navigator.language || (navigator.languages || ["en"])[0]
    moment.locale(language)
    document.documentElement.style.setProperty("--color-brand", this.theme)
  },
  watch: {
    page() {
      this.search = ""
      this.inAction = false
    },
    selected() {
      this.search = ""
    }
  }
}
</script>

<template>
  <div class="grid grid-cols-4 gap-6 w-full p-6 md:h-screen overflow-hidden">
    <div class="col-span-1 overflow-hidden">
      <ProjectCard/>
    </div>

    <div class="col-span-3 overflow-hidden">
      <div id="project-details" class="flex flex-col card h-full">
        
        <ul class="flex flex-wrap text-sm font-medium text-center border-b border-brand/60 space-x-1 -mt-3 -ml-3 mb-3">
          <li>
            <button type="button" class="inline-block p-4 uppercase" :class="{
              'text-brand/80 bg-brand/20': page === 'tasks',
              'text-brand/80 hover:bg-brand/10': page !== 'tasks'
            }" @click="page = 'tasks'">
              Tasks
            </button>
          </li>
          <li>
            <button type="button" class="inline-block p-4 uppercase" :class="{
              'text-brand/80 bg-brand/20': page === 'wages',
              'text-brand/80 hover:bg-brand/10': page !== 'wages'
            }" @click="page = 'wages'">
              Wages
            </button>
          </li>
          <li class="grow"></li>
          <li class="self-center">
            <Input label="Search" name="search" type="search" v-model="search" :disabled="!selected"/>
          </li>
        </ul>

        <router-view></router-view>
      </div>
    </div>
  </div>
</template>