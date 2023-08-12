<script>
import { mapState, mapActions } from 'pinia'
import { useProjectStore } from '@/stores/project'
import axios from "axios";

import TaskForm from '@/components/molecules/task/TaskForm.vue';
import TaskItem from '@/components/molecules/task/TaskItem.vue';
import {sortByDate} from "@/utils.js";
import ProjectItem from "@/components/molecules/project/ProjectItem.vue";
import TaskRemove from '../molecules/task/TaskRemove.vue';

export default {
  name: "TaskCard",
  data() {
    return {
      tasks: [],
      create: false,
      edit: 0,
      remove: 0
    };
  },
  computed: {
    groups() {
      if (!this.tasks) return


    },
    ...mapState(useProjectStore, {
      project: "id"
    })
  },
  methods: {
    async loadTasks() {
      if (!this.project) return;

      const response = await axios.get('/api/tasks', {
        params: { page: 1, per_page: 0, order_by: 'start', order: 'desc', project_id: this.project }
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
    async formRemoveSubmitted(id) {
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
  components: { ProjectItem, TaskForm, TaskItem, TaskRemove }
}
</script>

<template>
  <div class="flex flex-col overflow-hidden">
    <div class="overflow-y-scroll">
      <table class="w-full text-sm">
        <thead class="text-brand/70">
          <tr class="sticky top-0 bg-[#3e3121]">
            <th class="w-[30%] text-left">Status / Description</th>
            <th class="w-[20%] text-right">Start</th>
            <th class="w-[20%] text-right">End</th>
            <th class="w-[10%] text-right">Elapsed</th>
            <th class="w-[10%] text-right">Amount</th>
            <th class="w-[10%] text-right">Actions</th>
          </tr>
        </thead>
        <tbody class="text-brand/80">
          <template v-for="task in tasks" :key="task.id">
            <TaskItem v-if="edit !== task.id && remove !== task.id" :task="task"
                      @task:edit="edit = task.id" @task:remove="remove = task.id" 
                      :disabled="create || edit || remove"/>
            <TaskForm v-if="edit === task.id" :id="task.id" :name="task.name" :start="task.start" :end="task.end" :completed="task.completed"
                      @form:submitted="formEditSubmitted" @form:cancel="edit = 0"/>
            <TaskRemove v-if="remove === task.id" :id="task.id" :name="task.name" :start="task.start" 
                        @form:submitted="formRemoveSubmitted" @form:cancel="remove = 0"/>
          </template>
        </tbody>
        <tfoot class="sticky bottom-0 bg-[#3e3121]">
          <TaskForm v-if="create" @form:submitted="formCreateSubmitted" @form:cancel="create = false"/>
          <tr v-if="!create && !edit && !remove">
            <td colspan="6">
              <button type="button" class="btn btn-text text-sm uppercase w-full justify-center"
                      :disabled="edit || !project" @click="create = !create">
                <font-awesome-icon icon="fa-solid fa-plus" />
              </button>
            </td>
          </tr>
        </tfoot>
      </table>
    </div>
  </div>
</template>