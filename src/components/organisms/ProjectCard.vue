<script>
import axios from "axios";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

import ProjectItem from '@/components/molecules/project/ProjectItem.vue';
import ProjectForm from "@/components/molecules/project/ProjectForm.vue";

export default {
  name: "ProjectCard",
  components: {FontAwesomeIcon, ProjectItem, ProjectForm},
  data() {
    return {
      projects: [],
      edit: 0,
      create: false
    }
  },
  methods: {
    async loadProjects() {
      const response = await axios.get('/api/projects')
      const data = await response.data
      this.projects = data.items
    },
    async removeProject(id) {
      const response = await axios.delete(`/api/projects/${id}`)
      if (response.status !== 204) {
        return
      }
      this.projects = this.projects.filter((obj => obj.id !== id))
    },
    addProject(project) {
      this.create = false
      this.projects.push(project)
    },
    editProject(project) {
      const index = this.projects.findIndex((obj => obj.id === project.id))
      this.projects[index].name = project.name
      this.edit = 0
    }
  },
  async mounted() {
    this.loadProjects()
  }
}
</script>

<template>
  <div class="h-full flex flex-col card mb-3">
    <div class="flex items-center justify-between mb-3">
      <h1 class="font-medium text-lg md:text-xl leading-none text-brand/80 uppercase">
        Projects
      </h1>
      
      <button type="button" class="btn btn-brand text-xs uppercase" @click="this.create = !this.create">
        {{ create ? 'Cancel' : 'New' }}
      </button>
    </div>

    <div class="py-2 space-y-1">
      <template v-for="project in projects" :key="project.id">
        <ProjectItem v-if="edit !== project.id" :id="project.id" :name="project.name" 
          @project:edit="this.edit = project.id" @project:remove="this.removeProject"/>

        <ProjectForm v-else :id="project.id" :name="project.name" @form:submitted="this.editProject"/>

      </template>
      <ProjectForm v-if="create" @form:submitted="this.addProject"/>
    </div>
  </div>
</template>