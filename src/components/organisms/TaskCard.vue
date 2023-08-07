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
    formCreateSubmitted(task) {
      this.create = false
      this.tasks.unshift(task)
    },
    formEditSubmitted(task) {
      const index = this.tasks.findIndex((obj => obj.id === task.id))
      this.tasks[index] = task
      this.edit = 0
    },
    async removeTask(id) {
      const response = await axios.delete(`/api/tasks/${id}`)
      if (response.status !== 204) return;

      this.tasks = this.tasks.filter((obj => obj.id !== id));
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
        <template v-for="task in tasks" :key="task.id">
          <TaskItem v-if="edit !== task.id" :task="task"
                    @task:edit="edit = task.id"
                    @task:remove="removeTask"/>
          <TaskForm v-else :id="task.id" :name="task.name" :start="task.start" :end="task.end" :completed="task.completed"
                    @form:submitted="formCreateSubmitted" @form:cancel="edit = 0"/>
        </template>
        <TaskForm v-if="create" @form:submitted="formEditSubmitted" @form:cancel="create = false"/>
        <tr v-if="!create && !edit">
          <td colspan="6">
            <button type="button" class="btn btn-text text-sm uppercase w-full justify-center"
                    :disabled="edit || !project" @click="create = !create">
              <font-awesome-icon icon="fa-solid fa-plus" />
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>