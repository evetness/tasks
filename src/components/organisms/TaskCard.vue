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
      if (!this.project) return;

      const response = await axios.get('/api/tasks', {
        params: { project_id: this.project, order_by: 'start', order: 'desc' }
      });
      const data = await response.data;
      this.tasks = data.items;
    },
    addTask(task) {
      this.create = false
      this.tasks.unshift(task)
    },
    editTask(task) {
      const index = this.tasks.findIndex((obj => obj.id === task.id))
      this.tasks[index] = task
      this.edit = 0
    },
    formatCurrency,
  },
  mounted() {
    this.loadTasks();
  },
  watch: {
    project() {
      this.create = false;
      this.edit = 0;
      this.loadTasks();
    }
  },
  components: { TaskForm, TaskItem }
}
</script>

<template>
  <div class="flex flex-col h-full">
    <table class="w-full text-sm">
      <thead class="text-brand/70">
        <tr>
          <th class="w-[40%] text-left">Status / Description</th>
          <th class="w-[13%] text-right">Start</th>
          <th class="w-[13%] text-right">End</th>
          <th class="w-[12%] text-right">Elapsed</th>
          <th class="w-[12%] text-right">Amount</th>
          <th class="w-[10%] text-right">Actions</th>
        </tr>
      </thead>
      <tbody class="text-brand/80">
        <TaskForm v-if="this.create" @form:submitted="this.addTask"/>
        <TaskItem v-for="task in tasks" :key="task.id" :task="task"/>
      </tbody>
    </table>
    <button type="button" class="btn btn-brand text-xs uppercase w-full justify-center mt-auto" :disabled="this.edit || !this.project"
            @click="this.create = !this.create">
      {{ create ? 'Cancel' : 'New' }}
    </button>
  </div>
</template>