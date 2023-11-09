<script setup>
import moment from "moment/min/moment-with-locales";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectList from "@/components/organisms/ProjectList.vue";
import TaskList from '@/components/organisms/TaskList.vue';

import { watch } from 'vue';

import { storeToRefs } from 'pinia'
import { useSettingsStore } from "@/stores/settings.js";
import { useProjectStore } from '@/stores/project'
import { useGlobalStore } from "@/stores/global.js";

const settingsStore = useSettingsStore();
const { theme } = storeToRefs(settingsStore);

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const globalStore = useGlobalStore();
const { inAction } = storeToRefs(globalStore);

watch(selected, (newValue) => inAction.value = false);

const language = navigator.language || (navigator.languages || ["en"])[0];
moment.locale(language);
document.documentElement.style.setProperty("--color-brand", theme.value);
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