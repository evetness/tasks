<script setup>
import { watch } from 'vue';
import moment from "moment/min/moment-with-locales";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectList from "@/components/organisms/ProjectList.vue";
import TaskList from '@/components/organisms/TaskList.vue';
import Settings from "./components/organisms/Settings.vue";

import { storeToRefs } from 'pinia';
import { useSettingsStore } from "@/stores/settings.js";
import { useProjectStore } from "@/stores/project.js";
import { useStorage } from '@vueuse/core';
import { PROJECT_STORAGE } from './constants';

const settingsStore = useSettingsStore();
const { theme } = storeToRefs(settingsStore);
const { setIsOpen } = settingsStore;

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const language = navigator.language || (navigator.languages || ["en"])[0];
moment.locale(language);

const setRootProperty = () => {
  document.documentElement.style.setProperty("--color-brand", theme.value);
};
setRootProperty();

watch(theme, () => setRootProperty())
</script>

<template>
  <main class="p-4">
    <div class="container mx-auto">
      <div class="text-2xl font-extrabold text-brand mb-3 flex items-center gap-3 uppercase">
        <font-awesome-icon icon="folder" />
        Projects

        <button class="btn btn-text ml-auto" @click="setIsOpen(true)">
          <font-awesome-icon icon="gear" />
        </button>

      </div>
      <ProjectList />
      <template v-if="selected">
        <div class="text-xl font-extrabold text-brand my-3 flex items-center gap-3 uppercase">
          <font-awesome-icon icon="clipboard-list" />
          Tasks
        </div>
        <TaskList />
      </template>
    </div>
  </main>
  <Settings />
</template>