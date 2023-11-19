<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { inject } from 'vue';

import { storeToRefs } from "pinia";
import { useProjectStore } from "@/stores/project.js";

const emits = defineEmits(['form:close']);
const axios = inject('axios');

const projectStore = useProjectStore();
const { project } = storeToRefs(projectStore);

const submitForm = async () => {
  const response = await axios.delete(`/api/projects/${project.value.id}`)
  if (response.status !== 204) return;

  projectStore.removeProject(project.value.id);
  emits('form:close')
}
</script>

<template>
  <div class="group relative w-64 sm:w-72">
    <div class="text-brand text-sm text-center">
      <div class="h-7 w-24 sm:w-32 rounded-t-xl border-t-2 border-x-2 border-transparent bg-brand/20">
        <font-awesome-icon icon="trash-can" />
      </div>
    </div>
    <div class="flex items-center flex-wrap rounded-b-2xl rounded-tr-2xl border-2 border-transparent bg-brand/20">
      <div class="flex-auto p-4 text-brand">
        <form @submit.prevent="submitForm">
          <div class="h-12 overflow-ellipsis mt-1">
            <div class="flex leading-none">
              <font-awesome-icon icon="triangle-exclamation" size="lg" fixedWidth />
              <div class="ml-1 text-sm">
                Remove <span class="font-bold">{{ project.name }}</span>?
              </div>
            </div>
          </div>
          <div class="flex items-center gap-1 justify-end mt-1">
            <button type="submit" class="btn btn-text text-xs uppercase">
              <font-awesome-icon icon="fa-trash-can" fixedWidth />
              Remove
            </button>
            <button type="button" class="btn btn-text text-xs uppercase" @click="emits('form:close')">
              <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>