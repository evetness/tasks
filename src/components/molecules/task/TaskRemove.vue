<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import moment from 'moment/min/moment-with-locales';

import { defineProps, defineEmits, inject } from 'vue';

import { useTaskStore } from "@/stores/task.js";

const props = defineProps(['id', 'name', 'start']);
const emits = defineEmits(['form:close']);
const axios = inject('axios');

const taskStore = useTaskStore();
const { removeTask } = taskStore;

const submitForm = async () => {
  const response = await axios.delete(`/api/tasks/${props.id}`);
  if (response.status !== 204) return;
  removeTask(props.id);
  emits('form:close');
}
</script>

<template>
  <div class="group relative text-brand/80">
    <div class="w-full p-3 rounded-xl bg-brand/5 enabled:hover:bg-brand/10 enabled:focus:bg-brand/10">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <div class="text-sm">
          <div class="text-brand/90">
            <font-awesome-icon icon="triangle-exclamation" size="lg" fixedWidth />
            Remove <span class="font-bold">{{ name }}</span> task started at <span
              class="font-bold">{{ moment(start).format("lll") }}</span>?
          </div>
        </div>

        <form id="task-remove-form" @submit.prevent="submitForm" class="flex items-center justify-end ml-auto">
          <button type="submit" class="btn btn-text text-xs uppercase">
            <font-awesome-icon icon="fa-regular fa-trash-can" fixedWidth />
            Remove
          </button>
          <button type="button" class="btn btn-text text-xs uppercase" @click="emits('form:close')">
            <font-awesome-icon icon="fa-solid fa-xmark" fixedWidth />
            Cancel
          </button>
        </form>
      </div>
    </div>
  </div>
</template>