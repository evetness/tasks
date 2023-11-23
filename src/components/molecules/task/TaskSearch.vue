<script setup>
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Input from '@/components/atoms/Input.vue';

import { watch } from 'vue';
import { storeToRefs } from 'pinia';

import { useProjectStore } from '@/stores/project';
import { useTaskStore } from '@/stores/task';
import { TASK_INCOMPLETE, TASK_COMPLETED, TASK_STATES } from '@/constants';

const projectStore = useProjectStore();
const { selected } = storeToRefs(projectStore);

const taskStore = useTaskStore();
const { search, status } = storeToRefs(taskStore);
const { getTasks } = taskStore;

let timer = null;

const changeStatus = () => {
  const index = TASK_STATES.indexOf(status.value);
  if (index === (TASK_STATES.length - 1)) {
    status.value = TASK_STATES[0];
  } else {
    status.value = TASK_STATES[index + 1];
  }
};

watch(selected, () => {
  search.value = "";
  status.value = "INCOMPLETE";
});
watch(search, () => {
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
  timer = setTimeout(() => {
    getTasks();
  }, 400);
})
watch(status, () => getTasks());

</script>

<template>
  <form class="text-brand text-sm" @submit.prevent="">
    <div class="flex items-center gap-1">
      <Input name="search" type="text" v-model="search">
      <template #prefix>
        <font-awesome-icon icon="search" class="ml-2" />
      </template>
      </Input>

      <button type="button" class="btn btn-brand py-[9px] rounded" @click="changeStatus">
        <font-awesome-icon icon="circle-half-stroke" v-if="status === TASK_INCOMPLETE" />
        <font-awesome-icon icon="circle-check" v-if="status === TASK_COMPLETED" />
        <font-awesome-icon icon="infinity" v-if="status === null" />
      </button>
    </div>
  </form>
</template>