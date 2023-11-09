<script setup>
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import TaskAdd from '@/components/molecules/task/TaskAdd.vue';
import TaskForm from '@/components/molecules/task/TaskForm.vue';
import TaskItem from '@/components/molecules/task/TaskItem.vue';
import TaskRemove from '@/components/molecules/task/TaskRemove.vue';

import { ref, computed, watch, onMounted } from 'vue';
import { storeToRefs } from 'pinia';

import { useProjectStore } from '@/stores/project';
import { useGlobalStore } from "@/stores/global";
import { useTaskStore } from "@/stores/task.js";

const projectStore = useProjectStore();
const { selected, getUnpaidSalary } = storeToRefs(projectStore);

const taskStore = useTaskStore();
const { tasks } = storeToRefs(taskStore);
const { getTasks, changeTaskStatus } = taskStore;

const globalStore = useGlobalStore();
const { inAction, isTasksLoading } = storeToRefs(globalStore);
const { setAction } = globalStore;

const create = ref(false);
const edit = ref(0);
const remove = ref(0);
const open = ref(0);

const skeletonSize = computed(() => Math.floor(Math.random() * 10) + 1);

watch(selected, (newValue) => {
  create.value = false;
  edit.value = 0;
  remove.value = 0;
  getTasks();
});
watch(create, (newValue) => setAction(newValue));
watch(edit, (newValue) => setAction(newValue !== 0));
watch(remove, (newValue) => setAction(newValue !== 0));

onMounted(async () => await getTasks());
</script>

<template>
  <div class="flex flex-col gap-2 mt-2">
    <div class="flex items-center justify-between gap-1 text-2xs text-brand/70 font-medium px-3">
      <div class="text-left">Details</div>
      <div class="text-right">Amount</div>
    </div>

    <div class="space-y-1">
      <TaskForm v-if="create" @form:close="create = false" />
      <TaskAdd v-else class="w-full" @form:add="create = true" />

      <template v-if="isTasksLoading" v-for="n in skeletonSize">
        <div class="group relative rounded-xl bg-brand/5 w-full h-16">
          <div class="w-full p-3 flex items-center justify-between gap-2"></div>
        </div>
      </template>

      <template v-else v-for="task in tasks" :key="task.id">
        <TaskItem v-if="edit !== task.id && remove !== task.id" :task="task" @task:edit="edit = task.id"
          @task:remove="remove = task.id" @task:complete="changeTaskStatus(task.id)" :disabled="inAction" />

        <TaskForm v-if="edit === task.id" :id="task.id" :name="task.name" :start="task.start" :end="task.end"
          :completed="task.completed" @form:close="edit = 0" />

        <TaskRemove v-if="remove === task.id" :id="task.id" :name="task.name" :start="task.start"
          @form:close="this.remove = 0" />
      </template>
    </div>
  </div>
</template>