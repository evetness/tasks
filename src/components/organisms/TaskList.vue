<script>
import { mapActions, mapState } from 'pinia'
import { useProjectStore } from '@/stores/project'
import { useGlobalStore } from "@/stores/global";

import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import TaskForm from '@/components/molecules/task/TaskForm.vue';
import TaskItem from '@/components/molecules/task/TaskItem.vue';
import TaskRemove from '@/components/molecules/task/TaskRemove.vue';
import TaskSkeleton from "@/components/molecules/task/TaskSkeleton.vue";
import { useTaskStore } from "@/stores/task.js";

export default {
  name: "TaskList",
  data() {
    return {
      create: false,
      edit: 0,
      remove: 0,
      complete: false
    };
  },
  computed: {
    ...mapState(useTaskStore, ["tasks"]),
    ...mapState(useProjectStore, ["selected"]),
    ...mapState(useGlobalStore, ["inAction", "isTasksLoading"])
  },
  methods: {
    async loadTasks() {
      await this.getTasks();
    },
    ...mapActions(useTaskStore, ["getTasks"]),
    ...mapActions(useGlobalStore, ["setAction"])
  },
  async mounted() {
    await this.loadTasks()
  },
  watch: {
    search() {
      this.loadTasks()
    },
    selected() {
      this.create = false;
      this.edit = 0;
      this.remove = 0;
      this.loadTasks();
    },
    edit(newValue) {
      this.setAction(newValue !== 0);
    },
    create(newValue) {
      this.setAction(newValue)
    },
    remove(newValue) {
      this.setAction(newValue !== 0)
    }
  },
  components: { FontAwesomeIcon, TaskSkeleton, TaskForm, TaskItem, TaskRemove }
}
</script>

<template>
  <div class="flex flex-col gap-2 mt-2">
    <div class="flex items-center justify-between gap-1 text-2xs text-brand/70 font-medium px-3">
      <div class="text-left">Details</div>
      <div class="text-right">Amount</div>
    </div>

    <div class="space-y-1">
      <TaskSkeleton v-if="isTasksLoading" />
      <template v-else v-for="task in tasks" :key="task.id">
        <TaskItem v-if="edit !== task.id && remove !== task.id" :task="task" @task:edit="edit = task.id"
          @task:remove="remove = task.id" :disabled="inAction" />

        <TaskForm v-if="edit === task.id" :id="task.id" :name="task.name" :start="task.start" :end="task.end"
          :completed="task.completed" @form:close="edit = 0" />

        <TaskRemove v-if="remove === task.id" :id="task.id" :name="task.name" :start="task.start"
          @form:close="this.remove = 0" />
      </template>
      <div class="w-full">
        <TaskForm v-if="create" @form:close="create = false" />
        <button v-else type="button" class="btn btn-text text-sm uppercase w-full justify-center"
          :disabled="inAction || !selected" @click="create = true">
          <font-awesome-icon icon="fa-solid fa-plus" />
        </button>
      </div>
    </div>
  </div>
</template>