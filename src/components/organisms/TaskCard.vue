<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import TaskForm from '@/components/molecules/task/TaskForm.vue';
import TaskItem from '@/components/molecules/task/TaskItem.vue';
import {sortByDate} from "@/utils.js";
import ProjectItem from "@/components/molecules/project/ProjectItem.vue";

export default {
  name: "TaskCard",
  data() {
    return {
      tasks: [],
      create: false,
      edit: 0
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
    async formCreateSubmitted(task) {
      this.create = false
      this.tasks.push(task)
      this.tasks.sort((a, b) => sortByDate(a, b, "start"))
      await this.getUnpaidSalary()
    },
    async formEditSubmitted(task) {
      const index = this.tasks.findIndex((obj => obj.id === task.id))
      this.tasks[index] = task
      this.edit = 0
      await this.getUnpaidSalary()
    },
    async removeTask(id) {
      const response = await axios.delete(`/api/tasks/${id}`)
      if (response.status !== 204) return;

      this.tasks = this.tasks.filter((obj => obj.id !== id));
      await this.getUnpaidSalary()
    },
    ...mapActions(useProjectStore, ["getUnpaidSalary"])
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
  components: {ProjectItem, TaskForm, TaskItem }
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
                    @task:edit="edit = task.id" :can-edit="!create && !edit"
                    @task:remove="removeTask" :can-remove="!create && !edit"/>
          <TaskForm v-else :id="task.id" :name="task.name" :start="task.start" :end="task.end" :completed="task.completed"
                    @form:submitted="formEditSubmitted" @form:cancel="edit = 0"/>
        </template>
        <TaskForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="create = false"/>
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