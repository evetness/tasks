<script>
import { mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import { formatCurrency } from '@/utils';
import TaskForm from '../molecules/task/TaskForm.vue';

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
    formatCurrency,
  },
  watch: {
    project() {
      this.loadTasks();
    }
  },
  components: { TaskForm }
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
        <tr v-for="task in tasks" :key="task.id" class="group hover:bg-brand/20">
          <td class="text-xs text-left ">
            <div class="flex items-center gap-1">
              <font-awesome-icon v-if="!task.completed" icon="fa-regular fa-hourglass-half" size="xs" />
              <font-awesome-icon v-if="task.completed" icon="fa-regular fa-check-circle" size="xs" />
              {{ task.name }}
            </div>
          </td>
          <td class="text-xs text-right">{{ task.start }}</td>
          <td class="text-xs text-right">{{ task.end }}</td>
          <td class="text-xs text-right text-brand">{{ task.elapsed }}</td>
          <td class="text-xs text-right text-brand tracking-thighter font-extrabold group-hover:text-sm pr-1">
            {{ formatCurrency(task.amount, task.currency) }}
          </td>
          <td class="text-right">
            <button type="button" class="btn btn-text" @click="$emit('task:edit', this.id)">
              <font-awesome-icon icon="fa-regular fa-pen-to-square" />
            </button>
            
            <button type="button" class="btn btn-text" @click="$emit('task:remove', this.id)">
              <font-awesome-icon icon="fa-regular fa-trash-can" />
            </button>
          </td>
        </tr>
        <TaskForm v-if="this.create" />
      </tbody>
    </table>
  </div>
</template>