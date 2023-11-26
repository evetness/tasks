<script setup>
import { watch, onMounted } from 'vue';
import moment from "moment/min/moment-with-locales";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import ProjectList from "@/components/organisms/ProjectList.vue";
import TaskList from '@/components/organisms/TaskList.vue';
import Settings from "@/components/organisms/Settings.vue";
import Toast from '@/components/organisms/Toast.vue';

import { SETTINGS_PROJECT_ID, SETTINGS_REMEMBER_PROJECT, SETTINGS_THEME } from '@/constants.js';
import { storeToRefs } from 'pinia';
import { useSettingsStore } from "@/stores/settings.js";
import { useProjectStore } from "@/stores/project.js";
import { useGlobalStore } from '@/stores/global.js';
import { useToastStore } from '@/stores/toast.js';

const toastStore = useToastStore();
const { toasts, addToast, removeToast } = toastStore;

const settingsStore = useSettingsStore();
const { theme, rememberProject } = storeToRefs(settingsStore);
const { setIsOpen, getSetting } = settingsStore;

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const globalStore = useGlobalStore();
const { isSettingsLoading } = storeToRefs(globalStore);
const { setSettingsLoading } = globalStore;

const language = navigator.language || (navigator.languages || ["en"])[0];
moment.locale(language);

const setRootProperty = () => {
  document.documentElement.style.setProperty("--color-brand", theme.value);
};
setRootProperty();

watch(theme, () => setRootProperty());
onMounted(async () => {
  setSettingsLoading(true);
  const toastIndex = addToast('info-circle', 'Loading settings!', false, 0);
  const settingsTheme = await getSetting(SETTINGS_THEME, null);
  if (settingsTheme) theme.value = settingsTheme.content;

  const settingsRememberProject = await getSetting(SETTINGS_REMEMBER_PROJECT, null);
  if (settingsRememberProject) rememberProject.value = settingsRememberProject.content === 'true';

  const settingsSelectedProjectId = await getSetting(SETTINGS_PROJECT_ID, null)
  if (settingsSelectedProjectId) selected.value = Number(settingsSelectedProjectId.content);

  setSettingsLoading(false);
  removeToast(toastIndex);
  addToast('check-circle', 'Settings successfully loaded!', false, 2500);
})
</script>

<template>
  <Toast />
  <main class="p-4">
    <div class="container mx-auto">
      <div class="text-2xl font-extrabold text-brand mb-3 flex items-center gap-3 uppercase">
        <font-awesome-icon icon="folder" />
        Projects

        <button class="btn btn-text ml-auto" @click="setIsOpen(true)">
          <font-awesome-icon icon="gear" :spin="isSettingsLoading" />
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