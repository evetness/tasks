<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import { formatCurrency } from '@/utils';
import TaskForm from '../molecules/task/TaskForm.vue';
import TaskItem from '../molecules/task/TaskItem.vue';

export default {
  name: "TaskCard",
  data() {
    return {
      tasks: [],
      create: false,
      edit: false
    };
  },
  computed: {
    ...mapState(useProjectStore, {
      project: "id"
    })
  },
  methods: {
    async loadTasks() {
      const response = await axios.get('/api/tasks', {
        params: { project_id: this.project, order_by: 'start', order: 'desc' }
      });
      const data = await response.data;
      this.tasks = data.items;
    },
    addTask(task) {
      this.create = false
      this.tasks.push(task)
    },
    editTask(task) {
      const index = this.tasks.findIndex((obj => obj.id === task.id))
      this.tasks[index] = task
      this.edit = 0
    },
    formatCurrency,
  },
  watch: {
    project() {
      this.loadTasks();
    }
  },
  components: { TaskForm, TaskItem }
}
</script>

<template>
  <div class="h-full card">
    <div class="flex items-center justify-between mb-3">
      <h1 class="font-medium text-lg md:text-xl leading-none text-brand/80 uppercase">
        Tasks
      </h1>

      <button :disabled="this.edit || !this.project" type="button" class="btn btn-brand text-xs uppercase"
        @click="this.create = !this.create">
        {{ create ? 'Cancel' : 'New' }}
      </button>
    </div>

    <table class="w-full text-sm">
      <thead class="text-brand/70">
        <tr>
          <th class="w-[40%] text-left">Description</th>
          <th class="w-[13%] text-right">Start</th>
          <th class="w-[13%] text-right">End</th>
          <th class="w-[12%] text-right">Elapsed</th>
          <th class="w-[12%] text-right">Amount</th>
          <th class="w-[10%] text-right">Actions</th>
        </tr>
      </thead>
      <tbody class="text-brand/80">
        <TaskItem v-for="task in tasks" :key="task.id" :task="task"/>
        <TaskForm v-if="this.create" @form:submitted="this.addTask"/>
      </tbody>
    </table>
  </div>
</template>