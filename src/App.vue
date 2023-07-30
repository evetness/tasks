<script>
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import ProjectCreate from "@/components/molecules/project/ProjectCreate.vue";

export default {
  name: "App",
  components: {FontAwesomeIcon, ProjectCreate},
  data() {
    return {
      projects: [],
      tasks: [],
      selected: null,
      unpaid: null,
      wage: null,
    }
  },
  methods: {
    async loadProjects() {
      const response = await axios.get('/api/projects')
      const data = await response.data
      this.projects = data.items
    },
    async loadProjectWage(project_id) {
      const response = await axios.get(`/api/projects/${project_id}/current-salary`)
      const data = await response.data
      this.wage = data
    },
    async loadProjectUnpaidTasksAmount(project_id) {
      const response = await axios.get(`/api/projects/${project_id}/unpaid-tasks`)
      const data = await response.data
      this.unpaid = this.formatCurrency(data.amount, data.currency)
    },
    async loadTasks(project_id) {
      const response = await axios.get(
        '/api/tasks',
        {
          params: {project_id: project_id, order_by: 'start', order: 'desc'}
        }
      )
      const data = await response.data
      this.tasks = data.items
    },
    async selectProject(project_id) {
      this.selected = project_id
      this.loadTasks(project_id)
      this.loadProjectWage(project_id)
      this.loadProjectUnpaidTasksAmount(project_id)
    },
    formatCurrency(amount, currency) {
      const formatter = new Intl.NumberFormat('hu-HU', {
        style: 'currency',
        currency: currency,
      });
      return formatter.format(amount)
    }
  },
  async mounted() {
    this.loadProjects()
  }
}
</script>

<template>
  <div class="grid grid-cols-4 grid-rows-6 gap-6 w-full p-6 md:h-screen">
    <div class="col-span-1 row-start-1" :class="{'row-span-4': selected, 'row-span-full': !selected}">
      <div class="h-full card mb-3">
        <div class="flex items-center justify-between mb-3">
          <div class="header">Projects</div>
          <button class="btn btn-brand text-xs">
            ADD
          </button>
        </div>

        <ul class="text-brand/80 text-sm py-2 space-y-1">
          <li v-for="project in projects" :key="project.id" 
            class="flex items-center hover:bg-brand/20 focus:bg-brand/20 border-x" :class="{
              'border-transparent': !selected || selected != project.id,
              'border-brand/60 bg-brand/10': selected && selected == project.id
            }">
            <button class="w-full py-2 px-3 text-left text-brand" @click="this.selectProject(project.id)">
              {{ project.name }}
            </button>
            <button class="btn hover:bg-brand/20">
              <font-awesome-icon icon="fa-regular fa-pen-to-square" />
            </button>
            <button class="btn hover:bg-brand/20">
              <font-awesome-icon icon="fa-regular fa-trash-can" />
            </button>
          </li>
          <ProjectCreate />
        </ul>
      </div>
    </div>

    <div v-if="selected" class="col-span-1 row-start-5 row-span-2">
      <div class="h-full card flex flex-col">
        <div class="flex items-center justify-between mb-3">
          <div class="header">Wage</div>
          <button class="btn btn-brand text-xs uppercase">Add</button>
        </div>

        <div class="leading-none">
          <div class="text-sm text-brand/60 mb-1">Current Wage</div>
          <div v-if="wage" class="text-brand/80 font-medium">{{ this.formatCurrency(wage.amount, wage.currency) }}</div>
          <div v-if="wage" class="text-brand/50 text-xs">{{ this.wage.date }}</div>
        </div>

        <div class="mt-auto">
          <div class="text-sm text-brand/60">Unpaid</div>
          <div v-if="unpaid" class="text-brand text-xl font-bold">{{ unpaid }}</div>
        </div>

      </div>
    </div>

    <div class="col-span-3 row-span-full">
      <div class="h-full card">
        <div class="flex items-center justify-between mb-3">
          <div class="header">Tasks</div>
          <button class="btn btn-brand text-xs uppercase">Add</button>
        </div>

        <table class="w-full text-sm">
          <thead class="text-brand/70">
            <tr>
              <th class="w-2/6 text-left">Description</th>
              <th class="w-1/6 text-right">Start</th>
              <th class="w-1/6 text-right">End</th>
              <th class="w-1/6 text-right">Elapsed</th>
              <th class="w-1/6 text-right">Amount</th>
            </tr>
          </thead>
          <tbody class="text-brand/80">
            <tr v-for="task in tasks" :key="task.id" class="group hover:bg-brand/20">
              <td class="text-xs text-left py-1 pl-1 flex items-center gap-1">
                <font-awesome-icon v-if="!task.completed" icon="fa-regular fa-hourglass-half" size="xs" />
                <font-awesome-icon v-if="task.completed" icon="fa-regular fa-check-circle" size="xs"/>
                {{ task.name }}
              </td>
              <td class="text-xs text-right">{{ task.start }}</td>
              <td class="text-xs text-right">{{ task.end }}</td>
              <td class="text-xs text-right text-brand">{{ task.elapsed }}</td>
              <td class="text-xs text-right text-brand tracking-thighter font-extrabold group-hover:text-sm pr-1">{{ formatCurrency(task.amount, task.currency) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>