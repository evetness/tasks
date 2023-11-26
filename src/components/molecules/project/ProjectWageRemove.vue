<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import { inject } from 'vue';

import { storeToRefs } from "pinia";
import { useProjectStore } from "@/stores/project.js";
import { useTaskStore } from "@/stores/task.js";
import { useToastStore } from "@/stores/toast";

const emits = defineEmits(['form:close']);
const axios = inject('axios');

const projectStore = useProjectStore();
const { selected, amount } = storeToRefs(projectStore);
const { getCurrentWage, getUnpaidSalary } = projectStore;

const taskStore = useTaskStore();
const { getTasks } = taskStore;

const toastStore = useToastStore();
const { addToast }= toastStore;

const submitForm = async () => {
  const response = await axios.delete(`/api/projects/${selected.value}/wage`).catch((error) => {
    addToast('exclamation-triangle', 'Wage remove failed!', true, 5000);
    return null;
  })
  if (!response) return

  getCurrentWage();
  getUnpaidSalary();
  getTasks();
  addToast('check-circle', 'Wage successfully removed!', true, 2500);
  emits('form:close');
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
                Remove the current <span class="font-bold">{{ amount }}/h</span> wage?
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